import asyncio
import time
import aiohttp
import logging
import typing
import pathlib
import urllib.parse 
from PIL import Image
import subprocess
from resource.resource_queue import ResourceQueueBack

from monolith.infrastructure import execute_infrastructure
from resource.resource_queue import SimpleResourceQueue
from fs_resource_provider import FsResourceProvider
from resource.resource_provider import TimeBasedResourceProvider

logging.basicConfig(level=logging.INFO)


def is_image(path: pathlib.Path) -> bool:
    try:
        im = Image.open(path)
        im.verify()
    except Exception:
        return False


async def is_video(path: pathlib.Path):
    process = await asyncio.subprocess.create_subprocess_exec("ffprobe", ["-loglevel", "error", "-show_entries", "stream=codec_type", "-of default=nw=1"])
    result = await process.communicate()
    if process.returncode != 0:
        return False
    return "codec_type=video\n" in result[0].decode()
        


def make_provider_http(queue: ResourceQueueBack, interval: float, resource_tag: str, fs_path: str, url_prefix: str, **kwargs):
    class FsViaHttpProvider(FsResourceProvider):
        RESOURCE_TAG = resource_tag

        async def next_resource(self):
            result = await super().next_resource()
            result["payload"] = urllib.parse.urljoin(url_prefix, pathlib.Path(result["payload"]).name)
            return result
    
    return FsViaHttpProvider(queue, interval, fs_path, **kwargs)

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
            make_provider_http(queue, 10., "meme", "/mnt/nfs/memy.www", "http://internet.www/memy.www", filetype=is_image),
            make_provider_http(queue, 60., "commercial", "/mnt/nfs/youtube.com", "http://internet.www/youtube.com", filetype=is_video),
            UrlResourceProvider(queue, 5., (
                ("ser", "http://czyjestser.www/ser.txt"),
                ("mleko", "http://czyjestmleko.www/mleko.txt"),
                ("chleb", "http://czyjestchlebtostowy.www/chleb.txt"),
            ))
        )
    ))
    print(queue._content)
