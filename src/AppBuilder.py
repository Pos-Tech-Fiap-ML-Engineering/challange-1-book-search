from typing import Any
from collections.abc import Callable, Coroutine

from fastapi import FastAPI, APIRouter

import logging

from src.api.controllers.Router import Router
from src.api.controllers.abstractions.BaseController import BaseController
from src.api.controllers.v1.BooksController import BooksController
from src.api.controllers.v1.CategoriesController import CategoriesController
from src.api.controllers.v1.HealthController import HealthController
from src.api.controllers.v1.StatsController import StatsController
from src.application.boundaries.factory.HttpClientFactory import HttpClientFactory
from src.application.boundaries.use_case.UseCaseManager import UseCaseManager
from src.application.use_cases.book.get_book_by_id.GetBookByIdUseCaseImpl import (
    GetBookByIdUseCaseImpl,
)
from src.application.use_cases.book.get_book_stats.GetBookStatsUseCaseImpl import (
    GetBookStatsUseCaseImpl,
)
from src.application.use_cases.book.list_all_books.ListAllBooksUseCaseImpl import (
    ListAllBooksUseCaseImpl,
)
from src.application.use_cases.book.list_books_by_price_range.ListBooksByPriceRangeUseCaseImpl import (
    ListBooksByPriceRangeUseCaseImpl,
)
from src.application.use_cases.book.list_books_by_title_category.ListBooksByCategoryTitleUseCaseImpl import (
    ListBooksByCategoryTitleUseCaseImpl,
)
from src.application.use_cases.book.list_top_rated_books.ListTopRatedBooksUseCaseImpl import (
    ListTopRatedBooksUseCaseImpl,
)
from src.application.use_cases.book.scrape_books.ScrapeBooksUseCaseImpl import (
    ScrapeBooksUseCaseImpl,
)
from src.application.use_cases.book.scrape_books.ScrapeBooksUseCaseInput import (
    ScrapeBooksUseCaseInput,
)
from src.application.use_cases.category.list_categories.ListCategoriesUseCaseImpl import (
    ListCategoriesUseCaseImpl,
)
from src.application.use_cases.category.list_stats_books_by_categories.ListStatsBooksByCategoriesUseCaseImpl import (
    ListStatsBooksByCategoriesUseCaseImpl,
)
from src.domain.scrape_book.repository.ScrapeBookRepository import ScrapeBookRepository
from src.infrastructure.application.boundaries.factory.HttpClientFactoryImpl import (
    HttpClientFactoryImpl,
)
from src.infrastructure.application.boundaries.use_case.UseCaseManagerImpl import UseCaseManagerImpl
from src.infrastructure.domain.scrape_book.ScrapeBookRepositoryImpl import ScrapeBookRepositoryImpl
from src.infrastructure.standard.app_log.AppLoggerImpl import AppLoggerImpl
from src.scripts.presenters.ScrapeBooksUseCaseOutputPresenterImpl import (
    ScrapeBooksUseCaseOutputPresenterImpl,
)
from src.standard.app_log.AppLogger import AppLogger


class AppBuilder:
    V1_CONTROLLERS = "v1"

    def __init__(self) -> None:
        self._app_logger: AppLogger | None = None
        self._http_client_factory: HttpClientFactory | None = None
        self._scrape_book_repository: ScrapeBookRepository | None = None
        self._use_caser_manager: UseCaseManager | None = None
        self._controllers: dict[str, list[BaseController]] | None = None
        self._fast_api: FastAPI | None = None

    @property
    def app_logger(self) -> AppLogger:
        if not self._app_logger:
            self._app_logger = AppLoggerImpl(logger=logging.getLogger("app"))

        return self._app_logger

    @property
    def http_client_factory(self) -> HttpClientFactory:
        if not self._http_client_factory:
            self._http_client_factory = HttpClientFactoryImpl()

        return self._http_client_factory

    @property
    def scrape_book_repository(self) -> ScrapeBookRepository:
        if not self._scrape_book_repository:
            self._scrape_book_repository = ScrapeBookRepositoryImpl()

        return self._scrape_book_repository

    @property
    def use_caser_manager(self) -> UseCaseManager:
        if not self._use_caser_manager:
            self._use_caser_manager = UseCaseManagerImpl(
                logger=self.app_logger,
                use_cases=[
                    ScrapeBooksUseCaseImpl(
                        http_client_factory=self.http_client_factory,
                        scrape_book_repository=self.scrape_book_repository,
                    ),
                    ListAllBooksUseCaseImpl(scrape_book_repository=self.scrape_book_repository),
                    GetBookByIdUseCaseImpl(scrape_book_repository=self.scrape_book_repository),
                    ListBooksByCategoryTitleUseCaseImpl(
                        scrape_book_repository=self.scrape_book_repository
                    ),
                    ListCategoriesUseCaseImpl(scrape_book_repository=self.scrape_book_repository),
                    GetBookStatsUseCaseImpl(scrape_book_repository=self.scrape_book_repository),
                    ListStatsBooksByCategoriesUseCaseImpl(
                        scrape_book_repository=self.scrape_book_repository
                    ),
                    ListTopRatedBooksUseCaseImpl(
                        scrape_book_repository=self.scrape_book_repository
                    ),
                    ListBooksByPriceRangeUseCaseImpl(
                        scrape_book_repository=self.scrape_book_repository
                    ),
                ],
            )

        return self._use_caser_manager

    @property
    def controllers(self) -> dict[str, list[BaseController]]:
        if not self._controllers:
            self._controllers = {
                self.V1_CONTROLLERS: [
                    HealthController(),
                    BooksController(self.use_caser_manager),
                    CategoriesController(self.use_caser_manager),
                    StatsController(self.use_caser_manager),
                ]
            }

        return self._controllers

    @property
    def fast_api(self) -> FastAPI:
        if not self._fast_api:
            self._fast_api = FastAPI(
                title="Book Search",
                version="1.0.0",
                openapi_url="/openapi.json",
                docs_url="/docs",
                redoc_url="/redoc",
            )

            routers = Router.get_router(
                base_router=APIRouter(),
                v1_controllers=self.controllers[self.V1_CONTROLLERS],
            )
            self._fast_api.include_router(routers)

        return self._fast_api

    @property
    def script_scrape_books(self) -> Callable[[], Coroutine[Any, Any, None]]:
        async def _run() -> None:
            use_case_input = ScrapeBooksUseCaseInput()
            output: ScrapeBooksUseCaseOutputPresenterImpl = ScrapeBooksUseCaseOutputPresenterImpl()
            await self.use_caser_manager.execute_async(
                use_case_input, output, meta_information=None
            )
            await output.result_async()

        return _run

    def override_instances(
        self,
        param_app_logger: AppLogger | None = None,
        param_http_client_factory: HttpClientFactory | None = None,
        param_scrape_book_repository: ScrapeBookRepository | None = None,
        param_use_caser_manager: UseCaseManager | None = None,
        param_controllers: dict[str, list[BaseController]] | None = None,
        param_fast_api: FastAPI | None = None,
    ) -> None:
        self._app_logger = param_app_logger or self.app_logger
        self._http_client_factory = param_http_client_factory or self.http_client_factory
        self._scrape_book_repository = param_scrape_book_repository or self.scrape_book_repository
        self._use_caser_manager = param_use_caser_manager or self.use_caser_manager
        self._controllers = param_controllers or self.controllers
        self._fast_api = param_fast_api or self.fast_api
