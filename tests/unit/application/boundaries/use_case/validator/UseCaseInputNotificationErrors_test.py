import pytest

from src.application.boundaries.use_case.validator.UseCaseInputNotificationErrors import UseCaseInputNotificationErrors


class TestUseCaseInputNotificationErrors:
    _use_case_input_notification_errors: UseCaseInputNotificationErrors

    @pytest.fixture(autouse=True)
    def setup_teardown(self) -> None:
        self._use_case_input_notification_errors = UseCaseInputNotificationErrors.empty()

    def test_create_empty_use_case_input_notification_error(self) -> None:
        # arrange
        empty_errors = UseCaseInputNotificationErrors.empty()

        # act - assert
        assert empty_errors is not None
        assert empty_errors.has_errors is False
        assert len(empty_errors.errors) == 0

    def test_create_use_case_input_notification_errors_with_errors(self) -> None:
        # arrange - act
        self._use_case_input_notification_errors.add("prop1", "ERROR_1")
        self._use_case_input_notification_errors.add("prop1", "ERROR_2")
        self._use_case_input_notification_errors.add("prop1", "ERROR_3")

        self._use_case_input_notification_errors.add("prop2", "ERROR_1")
        self._use_case_input_notification_errors.add("prop2", "ERROR_2")
        self._use_case_input_notification_errors.add("prop2", "ERROR_3")

        self._use_case_input_notification_errors.add("prop3", "ERROR_1")
        self._use_case_input_notification_errors.add("prop3", "ERROR_2")
        self._use_case_input_notification_errors.add("prop3", "ERROR_3")

        # assert
        assert self._use_case_input_notification_errors.has_errors is True
        assert len(self._use_case_input_notification_errors.errors) == 3
        assert self._use_case_input_notification_errors.errors['prop1'] == ["ERROR_1", "ERROR_2", "ERROR_3"]
        assert self._use_case_input_notification_errors.errors['prop2'] == ["ERROR_1", "ERROR_2", "ERROR_3"]
        assert self._use_case_input_notification_errors.errors['prop3'] == ["ERROR_1", "ERROR_2", "ERROR_3"]
        assert self._use_case_input_notification_errors.flatten_errors == {'prop1_1': 'ERROR_1',
                                                                           'prop1_2': 'ERROR_2',
                                                                           'prop1_3': 'ERROR_3',
                                                                           'prop2_1': 'ERROR_1',
                                                                           'prop2_2': 'ERROR_2',
                                                                           'prop2_3': 'ERROR_3',
                                                                           'prop3_1': 'ERROR_1',
                                                                           'prop3_2': 'ERROR_2',
                                                                           'prop3_3': 'ERROR_3'}
