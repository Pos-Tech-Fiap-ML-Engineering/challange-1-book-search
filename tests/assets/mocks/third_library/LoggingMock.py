from unittest.mock import Mock
from pytest_mock import MockerFixture
from typing import cast

import logging

from src.standard.built_in.Static import Static
from tests.assets.utils.pytest.StrictMock import StrictMock


class LoggingMock(Static):
    @staticmethod
    def create(mocker: MockerFixture) -> Mock:
        return cast(Mock, StrictMock.make_strict_mock(logging.Logger, mocker=mocker))
