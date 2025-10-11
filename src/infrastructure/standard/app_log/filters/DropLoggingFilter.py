import logging

class DropLoggingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        path = getattr(record, "path", None)
        msg = (record.getMessage() or "").lower()

        if path and path.startswith("/api/v1/health"):
            return False
        if "/api/v1/health" in msg:
            return False

        ua = getattr(record, "user_agent", "")
        if isinstance(ua, str) and "elb-healthchecker" in ua.lower():
            return False

        return True
