from src.standard.error.ApplicationErrorCode import ApplicationErrorCode
from src.standard.error.ApplicationErrorInfo import ApplicationErrorInfo
from tests.assets.utils.helpers.ClassHelper import ClassHelper


class TestApplicationErrorInfo:
    def test_application_error_info(self) -> None:
        # arrange
        ex = Exception("CUSTOM ERROR")
        # - act
        error_info = ApplicationErrorInfo(
            code=ApplicationErrorCode.STANDARD_ERROR_USE_CASE_OUTPUT_NOT_HANDLER_INVALID_INPUT,
            message="Test error",
            cause={"error1": "FAIL"},
            error=ex,
        )

        state = ClassHelper.snapshot_state(error_info)

        # assert
        assert state == {
            "cause": {"error1": "FAIL"},
            "code": ApplicationErrorCode.STANDARD_ERROR_USE_CASE_OUTPUT_NOT_HANDLER_INVALID_INPUT,
            "error": ex,
            "message": "Test error",
        }
