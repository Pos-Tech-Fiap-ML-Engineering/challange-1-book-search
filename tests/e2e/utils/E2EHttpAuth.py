import base64
from collections.abc import AsyncGenerator

import httpx


class BasicAuthenticationTokenProvider:
    def __init__(self, username: str, password: str) -> None:
        self._username = username
        self._password = password
        self._credentials = f"{self._username}:{self._password}"

    async def generate_token_async(self) -> str:
        return base64.b64encode(self._credentials.encode('utf-8')).decode('utf-8')


class E2EHttpAuth(httpx.Auth):

    def __init__(self, token_provider: BasicAuthenticationTokenProvider) -> None:
        self._token_provider = token_provider

    async def async_auth_flow(self, request: httpx.Request) -> AsyncGenerator[httpx.Request, httpx.Response]:
        token = await self._token_provider.generate_token_async()
        request.headers["Authorization"] = f"Basic {token}"
        response = yield request
        if response.status_code in (401, 403):
            token = await self._token_provider.generate_token_async()
            request.headers["Authorization"] = f"Basic {token}"
            response = yield request

        return
