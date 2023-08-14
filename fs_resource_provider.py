import asyncio as aio
from pathlib import Path
import time
from typing import Callable

from containers.cyclic_queue import CyclicQueue
from resource.resource_queue import ResourceQueue
from resource.resource_provider import TimeBasedResourceProvider


Filetype = Callable[[Path], bool]
true = lambda p: True


class FsResourceProvider(TimeBasedResourceProvider):

    def __init__(self, queue: ResourceQueue, interval: float, directory: str, filetype: Filetype = true):
        super().__init__(queue, interval)
        self._directory = Path(directory)
        self._cyclic_queue: CyclicQueue[Path] = CyclicQueue()
        self._watcher_job: aio.Task | None = None
        self._filetype = filetype

    async def _worker(self):
        #  TODO: add filtering based on filetype
        while True:
            await aio.sleep(self._interval)
            for file in filter(self._filetype, self._directory.iterdir()):
                print(f"Adding {file}")
                self._cyclic_queue.add_item(file)

    async def setup(self):
        self._watcher_job = aio.create_task(self._worker())

    async def teardown(self):
        assert isinstance(self._watcher_job, aio.Task)
        self._watcher_job.cancel()

    async def next_resource(self) -> dict | None:
        next_media = self._cyclic_queue.next_media()
        if not next_media:
            return None
        return {
            "payload": str(next_media),
            "display_time": time.time(),
        }
