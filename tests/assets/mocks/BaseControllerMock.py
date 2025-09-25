from typing import cast
from unittest.mock import Mock

from pytest_mock import MockerFixture

from src.api.controllers.abstractions.BaseController import BaseController
from src.standard.built_in.Static import Static
from tests.assets.utils.pytest.StrictMock import StrictMock


class BaseControllerMock(Static):
    @staticmethod
    def create(mocker: MockerFixture) -> Mock:
        return cast(Mock, StrictMock.make_strict_mock(BaseController, mocker=mocker))