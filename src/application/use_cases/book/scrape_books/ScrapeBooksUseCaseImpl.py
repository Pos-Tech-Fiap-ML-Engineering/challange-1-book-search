import re
from typing import cast

import httpx
from bs4 import Tag, ResultSet, BeautifulSoup
from fake_useragent import UserAgent

from src.application.boundaries.factory.HttpClientFactory import HttpClientFactory
from src.application.boundaries.use_case.UseCase import UseCase
from src.application.use_cases.book.scrape_books.ScrapeBooksUseCaseInput import (
    ScrapeBooksUseCaseInput,
)
from src.application.use_cases.book.scrape_books.ScrapeBooksUseCaseOutputHandler import (
    ScrapeBooksUseCaseOutputHandler,
)
from src.domain.scrape_book.ScrapeBook import ScrapeBook
from src.domain.scrape_book.repository.ScrapeBookRepository import ScrapeBookRepository
from src.domain.scrape_book.vos.Money import Money
from src.domain.scrape_book.vos.Rating import Rating
from src.domain.scrape_book.vos.Upc import Upc
from src.standard.built_in.ListUtils import ListUtils


class ScrapeBooksUseCaseImpl(UseCase[ScrapeBooksUseCaseInput, ScrapeBooksUseCaseOutputHandler]):
    input_type: type[ScrapeBooksUseCaseInput] = ScrapeBooksUseCaseInput

    _BASE_URL: str = "https://books.toscrape.com"
    _RATING_MAPPING = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

    def __init__(
        self, http_client_factory: HttpClientFactory, scrape_book_repository: ScrapeBookRepository
    ) -> None:
        self._http_client = http_client_factory.create_async_factory(
            base_url=self._BASE_URL,
            timeout=httpx.Timeout(connect=5.0, read=15.0, write=10.0, pool=5.0),
            limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
        )
        self._scrape_book_repository = scrape_book_repository

        self.user_agent = UserAgent()

    async def execute_async(
        self,
        use_case_input: ScrapeBooksUseCaseInput,
        use_case_output: ScrapeBooksUseCaseOutputHandler,
    ) -> None:

        books, scraped_result = await self._scrape_books(use_case_output)

        if not scraped_result:
            return

        await self._scrape_book_repository.save_books_async(books)

        use_case_output.success()

    async def _fetch(self, url: str) -> httpx.Response:
        return await self._http_client.get(url, headers={"User-Agent": self.user_agent.random})

    async def _scrape_books(
        self, use_case_output: ScrapeBooksUseCaseOutputHandler
    ) -> tuple[list[ScrapeBook], bool]:
        current_url = self._BASE_URL
        books: list[ScrapeBook] = []
        scraped_books_result: bool = True

        while True:
            result = await self._fetch(current_url)

            if result.status_code != 200:
                use_case_output.failed_to_load_site()
                scraped_books_result = False
                break

            soup = BeautifulSoup(result.content, "html.parser")
            articles_link = soup.select("article.product_pod > h3 > a")

            books_scraped, scraped_content_result = await self._scrape_content_book(
                use_case_output, articles_link
            )

            if not scraped_content_result:
                scraped_books_result = False
                break

            books.extend(books_scraped)

            next_page_a = soup.select_one("ul.pager > li.next > a")
            next_page_url = str(next_page_a.get("href")) if next_page_a else None

            if not next_page_url:
                break

            current_url = f"{self._BASE_URL}/catalogue/{next_page_url.replace('catalogue/', '')}"

        return books, scraped_books_result

    async def _scrape_content_book(
        self, use_case_output: ScrapeBooksUseCaseOutputHandler, articles_link: ResultSet[Tag]
    ) -> tuple[list[ScrapeBook], bool]:
        books: list[ScrapeBook] = []
        for link in articles_link:
            url_href = str(link.get("href")).replace("catalogue/", "")
            book_content_url: str = f"{self._BASE_URL}/catalogue/{url_href}"
            result = await self._fetch(book_content_url)

            if result.status_code != 200:
                use_case_output.failed_to_load_link(book_content_url)
                return [], False

            soup = BeautifulSoup(result.content, "html.parser")

            books.append(
                ScrapeBook(
                    category=self._parse_scrape_book_category(soup),
                    title=self._parse_scrape_book_title(soup),
                    rating=Rating(self._parse_scrape_book_rating(soup)),
                    product_description=self._parse_scrape_product_description(soup),
                    upc=Upc(self._parse_scrape_upc(soup)),
                    product_type=self._parse_scrape_product_type(soup),
                    price_full=Money.from_float(self._parse_scrape_price_full(soup)),
                    price_excl_tax=Money.from_float(self._parse_scrape_price_excl_tax(soup)),
                    tax=Money.from_float(self._parse_scrape_price_tax(soup)),
                    availability=self._parse_scrape_availability(soup),
                    number_reviews=self._parse_scrape_number_reviews(soup),
                    image_url=self._parse_scrape_image_url(soup),
                    product_page_url=book_content_url,
                )
            )

        return books, True

    def _parse_scrape_book_category(self, soup: BeautifulSoup) -> str:
        return soup.select("ul.breadcrumb > li")[-2].get_text(strip=True)

    def _parse_scrape_book_title(self, soup: BeautifulSoup) -> str:
        return soup.select("ul.breadcrumb > li")[-1].get_text(strip=True)

    def _parse_scrape_book_rating(self, soup: BeautifulSoup) -> int:
        tag = cast(
            Tag,
            ListUtils.last(
                soup.select(
                    "article.product_page > div.row > div.col-sm-6.product_main > p.star-rating"
                )
            ),
        )

        rating_class = cast(list[str], tag.get("class"))[-1].strip()

        return self._RATING_MAPPING[rating_class]

    def _parse_scrape_product_description(self, soup: BeautifulSoup) -> str:
        product_description_p = soup.select_one("article.product_page > p")
        return product_description_p.get_text() if product_description_p else ""

    def _parse_scrape_upc(self, soup: BeautifulSoup) -> str:
        return next(
            cast(Tag, tr.find("td")).get_text(strip=True)
            for tr in soup.select(
                "article.product_page > table.table.table-striped > tr, "
                "article.product_page > table.table.table-striped > tbody > tr"
            )
            if cast(Tag, tr.find("th")).get_text(strip=True).lower() == "upc"
        )

    def _parse_scrape_product_type(self, soup: BeautifulSoup) -> str:
        return next(
            cast(Tag, tr.find("td")).get_text(strip=True)
            for tr in soup.select(
                "article.product_page > table.table.table-striped > tr, "
                "article.product_page > table.table.table-striped > tbody > tr"
            )
            if cast(Tag, tr.find("th")).get_text(strip=True).lower() == "product type"
        )

    def _parse_scrape_price_full(self, soup: BeautifulSoup) -> float:
        return next(
            float(cast(Tag, tr.find("td")).get_text(strip=True).replace("£", "").replace("Â", ""))
            for tr in soup.select(
                "article.product_page > table.table.table-striped > tr, "
                "article.product_page > table.table.table-striped > tbody > tr"
            )
            if cast(Tag, tr.find("th")).get_text(strip=True).lower() == "price (incl. tax)"
        )

    def _parse_scrape_price_excl_tax(self, soup: BeautifulSoup) -> float:
        return next(
            float(cast(Tag, tr.find("td")).get_text(strip=True).replace("£", "").replace("Â", ""))
            for tr in soup.select(
                "article.product_page > table.table.table-striped > tr, "
                "article.product_page > table.table.table-striped > tbody > tr"
            )
            if cast(Tag, tr.find("th")).get_text(strip=True).lower() == "price (excl. tax)"
        )

    def _parse_scrape_price_tax(self, soup: BeautifulSoup) -> float:
        return next(
            float(cast(Tag, tr.find("td")).get_text(strip=True).replace("£", "").replace("Â", ""))
            for tr in soup.select(
                "article.product_page > table.table.table-striped > tr, "
                "article.product_page > table.table.table-striped > tbody > tr"
            )
            if cast(Tag, tr.find("th")).get_text(strip=True).lower() == "tax"
        )

    def _parse_scrape_availability(self, soup: BeautifulSoup) -> int:
        return next(
            (
                int(m.group(1))
                if (
                    m := re.search(
                        r"\((\d+)\s+available\)", cast(Tag, tr.find("td")).get_text(strip=True)
                    )
                )
                else 0
            )
            for tr in soup.select(
                "article.product_page > table.table.table-striped > tr, "
                "article.product_page > table.table.table-striped > tbody > tr"
            )
            if cast(Tag, tr.find("th")).get_text(strip=True).lower() == "availability"
        )

    def _parse_scrape_number_reviews(self, soup: BeautifulSoup) -> int:
        return next(
            int(cast(Tag, tr.find("td")).get_text(strip=True))
            for tr in soup.select(
                "article.product_page > table.table.table-striped > tr, "
                "article.product_page > table.table.table-striped > tbody > tr"
            )
            if cast(Tag, tr.find("th")).get_text(strip=True).lower() == "number of reviews"
        )

    def _parse_scrape_image_url(self, soup: BeautifulSoup) -> str:
        img = cast(str, soup.select("div.item.active > img")[-1].get("src")).replace("../../", "")
        return f"{self._BASE_URL}/{img}"
