from __future__ import annotations

import logging

import pytest
from pytest_mock import MockerFixture
from unittest.mock import Mock
from collections.abc import Iterator

from src.infrastructure.standard.app_log.AppLoggerImpl import AppLoggerImpl
from src.standard.app_log.AppLogger import AppLogger
from tests.assets.mocks.third_library.LoggingMock import LoggingMock


class TestAppLoggerImpl:
    _msg = "test message"

    logging_mock: Mock
    app_logger: AppLogger

    @pytest.fixture(autouse=True)
    def setup_teardown(
        self, request: pytest.FixtureRequest, mocker: MockerFixture
    ) -> Iterator[None]:
        self.logging_mock = LoggingMock.create(mocker)
        self.app_logger = AppLoggerImpl(self.logging_mock)
        yield

    @pytest.mark.parametrize(
        ("method_name", "logger_level"),
        [
            ("debug", logging.DEBUG),
            ("info", logging.INFO),
            ("warn", logging.WARN),
            ("error", logging.ERROR),
        ],
        ids=[
            f"debug->{logging.DEBUG}",
            f"info->{logging.INFO}",
            f"warn->{logging.WARN}",
            f"error->{logging.ERROR}",
        ],
    )
    @pytest.mark.parametrize(
        ("extra_in", "expected_extra"),
        [(None, {}), ({"a": "1", "b": "2"}, {"a": "1", "b": "2"})],
        ids=["no-extra-attributes", "with-extra-attributes"],
    )
    def test_log_level_forwarding(
        self,
        method_name: str,
        logger_level: int,
        extra_in: dict[str, str],
        expected_extra: dict[str, str],
    ) -> None:
        # arrange
        self.logging_mock.log.side_effect = None
        self.logging_mock.log.return_value = None

        # act
        getattr(self.app_logger, method_name)(self._msg, extra_in)

        # assert
        self.logging_mock.log.assert_called_once_with(
            logger_level, self._msg, exc_info=None, extra=expected_extra
        )

    def test_log_level_error_with_error(self) -> None:
        # arrange

        exception = Exception("Fail")

        self.logging_mock.log.side_effect = None
        self.logging_mock.log.return_value = None

        # act
        self.app_logger.error(self._msg, extra={"error": "True"}, exc_info=exception)

        # assert
        self.logging_mock.log.assert_called_once_with(
            logging.ERROR,
            self._msg,
            extra={"error": "True"},
            exc_info=exception,
        )

    def test_new_scope(self, mocker: MockerFixture) -> None:
        # arrange
        scope_name = "test"

        child_scope = LoggingMock.create(mocker)

        self.logging_mock.getChild.side_effect = None
        self.logging_mock.getChild.return_value = child_scope

        child_scope.log.side_effect = None
        child_scope.log.return_value = None

        # act
        with self.app_logger.new_scope(scope_name, extra={"a": "1", "b": "2"}):
            self.app_logger.info(self._msg)

        # assert
        self.logging_mock.getChild.assert_called_once_with(scope_name)

        args, kwargs = child_scope.log.call_args
        assert args[0] == logging.INFO
        assert args[1] == self._msg
        assert kwargs["exc_info"] is None

        extra = kwargs["extra"]
        assert isinstance(extra, dict)
        assert len(extra) == 3
        assert list(extra.keys())[0].startswith(f"{scope_name}-")
        assert extra["a"] == "1"
        assert extra["b"] == "2"

    def test_new_scope_with_nested_scopes(self, mocker: MockerFixture) -> None:
        # arrange
        scope_name_1 = "test"
        scope_name_2 = "test-nested-1"
        scope_name_3 = "test-nested-2"

        child_scope_nested_3 = LoggingMock.create(mocker)
        child_scope_nested_3.log.side_effect = None
        child_scope_nested_3.log.return_value = None

        child_scope_nested_2 = LoggingMock.create(mocker)
        child_scope_nested_2.getChild.side_effect = None
        child_scope_nested_2.getChild.return_value = child_scope_nested_3
        child_scope_nested_2.log.side_effect = None
        child_scope_nested_2.log.return_value = None

        child_scope_nested_1 = LoggingMock.create(mocker)
        child_scope_nested_1.getChild.side_effect = None
        child_scope_nested_1.getChild.return_value = child_scope_nested_2
        child_scope_nested_1.log.side_effect = None
        child_scope_nested_1.log.return_value = None

        self.logging_mock.getChild.side_effect = None
        self.logging_mock.getChild.return_value = child_scope_nested_1

        # act
        with self.app_logger.new_scope(scope_name_1, extra={"a": "1", "b": "2"}):
            self.app_logger.info(self._msg, extra={"prop1": "1", "prop2": "2"})

            with self.app_logger.new_scope(scope_name_2, extra={"c": "3", "d": "4"}):
                self.app_logger.info(self._msg, extra={"prop3": "1", "prop4": "2"})

                with self.app_logger.new_scope(scope_name_3, extra={"d": "5", "e": "6"}):
                    self.app_logger.info(self._msg, extra={"prop5": "1", "prop6": "2"})

        # assert

        # self.logging_mock
        self.logging_mock.getChild.assert_called_once_with(scope_name_1)

        # child_scope_nested_1
        child_scope_nested_1.getChild.assert_called_once_with(scope_name_2)

        args, kwargs = child_scope_nested_1.log.call_args
        assert args[0] == logging.INFO
        assert args[1] == self._msg
        assert kwargs["exc_info"] is None

        extra = kwargs["extra"]
        assert isinstance(extra, dict)
        assert len(extra) == 5
        assert list(extra.keys())[0].startswith(f"{scope_name_1}-")
        assert extra["a"] == "1"
        assert extra["b"] == "2"
        assert extra["prop1"] == "1"
        assert extra["prop2"] == "2"

        # child_scope_nested_2
        child_scope_nested_2.getChild.assert_called_once_with(scope_name_3)

        args, kwargs = child_scope_nested_2.log.call_args
        assert args[0] == logging.INFO
        assert args[1] == self._msg
        assert kwargs["exc_info"] is None

        extra = kwargs["extra"]
        assert isinstance(extra, dict)
        assert len(extra) == 8
        assert list(extra.keys())[0].startswith(f"{scope_name_2}-")
        assert list(extra.keys())[1].startswith(f"{scope_name_1}-")
        assert extra["a"] == "1"
        assert extra["b"] == "2"
        assert extra["c"] == "3"
        assert extra["d"] == "4"
        assert extra["prop3"] == "1"
        assert extra["prop4"] == "2"

        # child_scope_nested_3
        args, kwargs = child_scope_nested_3.log.call_args
        assert args[0] == logging.INFO
        assert args[1] == self._msg
        assert kwargs["exc_info"] is None

        extra = kwargs["extra"]
        assert isinstance(extra, dict)
        assert len(extra) == 10
        assert list(extra.keys())[0].startswith(f"{scope_name_3}-")
        assert list(extra.keys())[1].startswith(f"{scope_name_2}-")
        assert list(extra.keys())[2].startswith(f"{scope_name_1}-")
        assert extra["a"] == "1"
        assert extra["b"] == "2"
        assert extra["c"] == "3"
        assert extra["d"] == "5"
        assert extra["e"] == "6"
        assert extra["prop5"] == "1"
        assert extra["prop6"] == "2"
