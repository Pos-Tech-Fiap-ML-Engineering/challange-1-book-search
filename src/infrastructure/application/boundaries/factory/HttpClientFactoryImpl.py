import httpx
from httpx._config import DEFAULT_LIMITS

from src.application.boundaries.factory.HttpClientFactory import HttpClientFactory
from httpx import AsyncClient, Timeout, Limits


class HttpClientFactoryImpl(HttpClientFactory):
    def create_async_factory(
        self, base_url: str, timeout: Timeout | None = None, limits: Limits | None = None
    ) -> httpx.AsyncClient:
        return AsyncClient(base_url=base_url, timeout=timeout, limits=(limits or DEFAULT_LIMITS))
