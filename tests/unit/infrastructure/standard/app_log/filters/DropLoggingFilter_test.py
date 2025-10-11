from __future__ import annotations

import logging
from typing import Optional, Any

import pytest

from src.infrastructure.standard.app_log.filters.DropLoggingFilter import DropLoggingFilter


def make_record(
    msg: Optional[str],
    *,
    level: int = logging.INFO,
    path: Optional[str] = None,
    user_agent: Optional[Any] = None,
    name: str = "test",
    pathname: str = __file__,
    lineno: int = 1,
) -> logging.LogRecord:
    rec = logging.LogRecord(
        name=name,
        level=level,
        pathname=pathname,
        lineno=lineno,
        msg=msg,
        args=(),
        exc_info=None,
    )
    if path is not None:
        setattr(rec, "path", path)
    if user_agent is not None:
        setattr(rec, "user_agent", user_agent)
    return rec


class TestDropLoggingFilter:

    @pytest.fixture(scope="function")
    def flt(self) -> DropLoggingFilter:
        return DropLoggingFilter()

    def test_allow_regular_message_no_extras(self, flt: DropLoggingFilter) -> None:
        # arrange - act
        rec = make_record("user did something")

        # assert
        assert flt.filter(rec) is True

    def test_allow_non_health_path(self, flt: DropLoggingFilter) -> None:
        # arrange - act
        rec = make_record("GET /api/v1/books", path="/api/v1/books")

        # assert
        assert flt.filter(rec) is True

    def test_allow_when_user_agent_is_not_string(self, flt: DropLoggingFilter) -> None:
        # arrange - act - assert
        rec_obj = make_record("ping", user_agent={"ua": "ELB-HealthChecker/2.0"})
        assert flt.filter(rec_obj) is True

        rec_none = make_record("ping", user_agent=None)
        assert flt.filter(rec_none) is True

    def test_allow_message_none(self, flt: DropLoggingFilter) -> None:
        # arrange - act
        rec = make_record(None)

        # assert
        assert flt.filter(rec) is True

    @pytest.mark.parametrize(
        "path",
        [
            "/api/v1/health",
            "/api/v1/health/",
            "/api/v1/healthz",
            "/api/v1/health/live",
            "/api/v1/healthcheck",
        ],
    )
    def test_drop_by_path_prefix(self, flt: DropLoggingFilter, path: str) -> None:
        # arrange - act
        rec = make_record("any", path=path)

        # assert
        assert flt.filter(rec) is False

    def test_keep_when_path_similar_but_not_prefix(self, flt: DropLoggingFilter) -> None:
        # arrange - act
        rec = make_record("GET /x/api/v1/health", path="/x/api/v1/health")

        # assert
        assert flt.filter(rec) is False

    @pytest.mark.parametrize(
        "msg",
        [
            "GET /api/v1/health 200",
            "ok /API/v1/HEALTH live",
            "status: ... /api/v1/health ...",
        ],
    )
    def test_drop_by_message_contains(self, flt: DropLoggingFilter, msg: str) -> None:
        # arrange - act
        rec = make_record(msg)

        # assert
        assert flt.filter(rec) is False

    def test_keep_when_message_does_not_contain_health(self, flt: DropLoggingFilter) -> None:
        # arrange - act
        rec = make_record("healthiness is good")  # não contém /api/v1/health

        # assert
        assert flt.filter(rec) is True

    @pytest.mark.parametrize(
        "ua",
        [
            "ELB-HealthChecker/2.0",
            "elb-healthchecker",
            "SomeAgent elb-healthchecker probe",
            "ELB-HEALTHCHECKER",
        ],
    )
    def test_drop_by_user_agent_elb_healthchecker(self, flt: DropLoggingFilter, ua: str) -> None:
        # arrange - act
        rec = make_record("ping", user_agent=ua)

        # assert
        assert flt.filter(rec) is False

    def test_keep_other_user_agents(self, flt: DropLoggingFilter) -> None:
        # arrange - act
        rec = make_record("ping", user_agent="curl/8.5.0")

        # assert
        assert flt.filter(rec) is True

    def test_drop_if_any_rule_matches_path_priority(self, flt: DropLoggingFilter) -> None:
        # arrange - act
        rec = make_record("normal message", path="/api/v1/health/live", user_agent="curl/8.0")

        # assert
        assert flt.filter(rec) is False

    def test_drop_if_any_rule_matches_message_priority(self, flt: DropLoggingFilter) -> None:
        # arrange - act
        rec = make_record("GET /api/v1/health", path="/not/health")

        # assert
        assert flt.filter(rec) is False

    def test_drop_if_any_rule_matches_user_agent_priority(self, flt: DropLoggingFilter) -> None:
        # arrange - act
        rec = make_record("ok", user_agent="elb-healthchecker/2.0", path="/api/v1/books")

        # assert
        assert flt.filter(rec) is False

    def test_integration_logger_filter_attached(self) -> None:
        # arrange
        logger = logging.getLogger("drop_filter_test_class")
        logger.setLevel(logging.INFO)

        captured: list[logging.LogRecord] = []

        class _Handler(logging.Handler):
            def emit(self, record: logging.LogRecord) -> None:
                captured.append(record)

        handler = _Handler()

        # act
        handler.addFilter(DropLoggingFilter())
        logger.addHandler(handler)

        # 1) DROP by path
        logger.handle(make_record("anything", path="/api/v1/health"))

        # 2) PASS
        logger.handle(make_record("something else", path="/api/v1/books"))

        # 3) DROP by UA
        logger.handle(make_record("ping", user_agent="ELB-HEALTHCHECKER"))

        # 4) DROP by message
        logger.handle(make_record("GET /api/v1/health 200"))

        # assert
        assert len(captured) == 1
        assert captured[0].getMessage() == "something else"
