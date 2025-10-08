from __future__ import annotations

import pytest

from src.scripts.presenters.ScrapeBooksUseCaseOutputPresenterImpl import (
    ScrapeBooksUseCaseOutputPresenterImpl,
)


class TestScrapeBooksUseCaseOutputPresenterImpl:

    async def test_initial_state_result_async_raises_not_implemented(self) -> None:
        # arrange
        presenter = ScrapeBooksUseCaseOutputPresenterImpl()

        # act - assert
        with pytest.raises(NotImplementedError):
            await presenter.result_async()

    async def test_success_sets_noop_handler_and_result_async_passes(self) -> None:
        # arrange
        presenter = ScrapeBooksUseCaseOutputPresenterImpl()

        # act
        presenter.success()

        # assert
        await presenter.result_async()

    async def test_failed_to_load_site_sets_handler_that_raises(self) -> None:
        # arrange
        presenter = ScrapeBooksUseCaseOutputPresenterImpl()

        # act
        presenter.failed_to_load_site()

        # assert
        with pytest.raises(Exception) as exc_info:
            await presenter.result_async()

        assert "Failed to load site" in str(exc_info.value)

    async def test_failed_to_load_link_sets_handler_that_raises_with_link(self) -> None:
        # arrange
        presenter = ScrapeBooksUseCaseOutputPresenterImpl()
        link = "http://example.com/page"

        # act
        presenter.failed_to_load_link(link)

        # assert
        with pytest.raises(Exception) as exc_info:
            await presenter.result_async()

        assert f"Failed to load link: {link}" in str(exc_info.value)
