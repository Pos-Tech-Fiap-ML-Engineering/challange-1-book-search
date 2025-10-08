from __future__ import annotations

import asyncio

from src.AppBuilder import AppBuilder

app_builder = AppBuilder()
script_scrape_books = app_builder.script_scrape_books


if __name__ == "__main__":
    asyncio.run(script_scrape_books())
