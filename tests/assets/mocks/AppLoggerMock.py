from unittest.mock import Mock
from pytest_mock import MockerFixture
from typing import cast

from src.standard.app_log.AppLogger import AppLogger
from src.standard.built_in.Static import Static
from tests.assets.utils.pytest.StrictMock import StrictMock


class AppLoggerMock(Static):
    @staticmethod
    def create(mocker: MockerFixture) -> Mock:
        return cast(Mock, StrictMock.make_strict_mock(AppLogger, mocker=mocker))
