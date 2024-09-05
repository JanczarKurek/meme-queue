import typing

import aiohttp

from resource.resource_provider import TimeBasedResourceProvider


class UrlResourceProvider(TimeBasedResourceProvider):
    """Queries a number of URLs"""
    def default_tag(self) -> str:
        return "status"

    def __init__(self, *, urls: typing.Iterable[tuple[str, str]], **kwargs):
        self._urls = tuple(urls)
        super().__init__(**kwargs)

    async def next_resource(self):
        payload = {}
        for name, url in self._urls:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        payload[name] = await resp.text()
            except Exception:
                payload[name] = None
        return {
            "payload": payload,
        }
