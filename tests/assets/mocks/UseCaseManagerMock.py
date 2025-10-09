from typing import cast
from unittest.mock import Mock

from pytest_mock import MockerFixture

from src.application.boundaries.use_case.UseCaseManager import UseCaseManager
from src.standard.built_in.Static import Static
from tests.assets.utils.pytest.StrictMock import StrictMock


class UseCaseManagerMock(Static):
    @staticmethod
    def create(mocker: MockerFixture) -> Mock:
        return cast(Mock, StrictMock.make_strict_mock(UseCaseManager, mocker=mocker))