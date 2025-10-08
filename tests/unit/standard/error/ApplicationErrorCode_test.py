from src.standard.error.ApplicationErrorCode import ApplicationErrorCode
from tests.assets.utils.pytest.CustomAsserts import CustomAsserts


class TestApplicationErrorCode:
    def test_validate_enum(self) -> None:
        # arrange
        CustomAsserts.assert_enum(
            ApplicationErrorCode,
            [
                "STANDARD_ERROR_USE_CASE_NOT_FOUND",
                "STANDARD_ERROR_USE_CASE_OUTPUT_NOT_HANDLER_INVALID_INPUT",
                "STANDARD_ERROR_USE_CASE_INPUT_INVALID_TYPE",
                "STANDARD_ERROR_USE_CASE_OUTPUT_HANDLER_INVALID_TYPE",
            ],
            [
                "1-1",
                "1-2",
                "1-3",
                "1-4",
            ],
        )
