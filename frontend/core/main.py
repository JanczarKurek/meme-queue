import asyncio
import time
import aiohttp
import logging
import typing
import pathlib
from resource.resource_queue import ResourceQueueBack

from monolith.infrastructure import execute_infrastructure
from resource.resource_queue import SimpleResourceQueue
from fs_resource_provider import FsResourceProvider
from resource.resource_provider import TimeBasedResourceProvider

logging.basicConfig(level=logging.INFO)


class ImageFsProvider(FsResourceProvider):
    RESOURCE_TAG = "meme"

    async def next_resource(self):
        result = await super().next_resource()
        result["payload"] = "http://internet.www/memy.www/" + pathlib.Path(result["payload"]).name
        return result

class UrlResourceProvider(TimeBasedResourceProvider):
    """Queries a number of URLs"""
    RESOURCE_TAG = "status"

    def __init__(self, queue: ResourceQueueBack, interval: float, urls: typing.Iterable[tuple[str, str]]):
        self._urls = tuple(urls)
        super().__init__(queue, interval)

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
            "display_time": time.time()
        }


if __name__ == "__main__":
    queue = SimpleResourceQueue(10)
    asyncio.run(execute_infrastructure(queue, 
        (
            ImageFsProvider(queue, 10., "/mnt/nfs/memy.www"),
            UrlResourceProvider(queue, 5., (
                ("ser", "http://czyjestser.www/ser.txt"),
                ("mleko", "http://czyjestmleko.www/mleko.txt"),
                ("chleb", "http://czyjestchlebtostowy.www/chleb.txt"),
            ))
        )
    ))
    print(queue._content)
