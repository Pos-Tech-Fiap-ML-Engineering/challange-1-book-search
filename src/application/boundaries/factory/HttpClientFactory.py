import abc

import httpx

from src.standard.built_in.Abstract import Abstract


class HttpClientFactory(Abstract):
    @abc.abstractmethod
    def create_async_factory(
        self,
        base_url: str,
        timeout: httpx.Timeout | None = None,
        limits: httpx.Limits | None = None,
    ) -> httpx.AsyncClient:
        pass
