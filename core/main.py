import asyncio
import logging

from monolith.infrastructure import execute_infrastructure
from resource.resource_queue import SimpleResourceQueue
from fs_resource_provider import FsResourceProvider

logging.basicConfig(level=logging.INFO)


class ImageFsProvider(FsResourceProvider):
    RESOURCE_TAG = "meme"

    # def next_resource(self) -> asyncio.Coroutine[asyncio.Any, asyncio.Any, dict | None]:
    #     result = super().next_resource()
    #     result["payload"] = ""


if __name__ == "__main__":
    queue = SimpleResourceQueue(10)
    asyncio.run(execute_infrastructure(queue, (ImageFsProvider(queue, 2., "/mnt/nfs/memy.www"),)))
    print(queue._content)
