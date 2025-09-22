from src.standard.error.ApplicationErrorCode import ApplicationErrorCode
from tests.assets.utils.pytest.CustomAsserts import CustomAsserts


class TestApplicationErrorCode:
    def test_validate_enum(self) -> None:
        # arrange
        CustomAsserts.assert_enum(ApplicationErrorCode,
                                  [
                                     "STANDARD_ERROR_USE_CASE_NOT_FOUND",
                                     "STANDARD_ERROR_USE_CASE_OUTPUT_NOT_HANDLER_INVALID_INPUT"]
                                  ,
                                  [
                                     "1-1",
                                     "1-2",
                                 ])
