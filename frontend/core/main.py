import asyncio
import logging
import pathlib

from monolith.infrastructure import execute_infrastructure
from resource.resource_queue import SimpleResourceQueue
from fs_resource_provider import FsResourceProvider

logging.basicConfig(level=logging.INFO)


class ImageFsProvider(FsResourceProvider):
    RESOURCE_TAG = "meme"

    async def next_resource(self):
        result = await super().next_resource()
        result["payload"] = "http://internet.www/memy.www/" + pathlib.Path(result["payload"]).name
        return 


if __name__ == "__main__":
    queue = SimpleResourceQueue(10)
    asyncio.run(execute_infrastructure(queue, (ImageFsProvider(queue, 10., "/mnt/nfs/memy.www"),)))
    print(queue._content)
