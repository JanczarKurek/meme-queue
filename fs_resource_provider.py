import asyncio as aio
import logging
from pathlib import Path
import time
from typing import Callable

from containers.cyclic_queue import CyclicQueue
from resource.resource_queue import ResourceQueueBack
from resource.resource_provider import TimeBasedResourceProvider

base_logger = logging.getLogger(__name__)
Filetype = Callable[[Path], bool]
true = lambda p: True


class FsResourceProvider(TimeBasedResourceProvider):
    """Serves data from a given folder cycling through it"""

    def __init__(self, queue: ResourceQueueBack, interval: float, directory: str, filetype: Filetype = true):
        super().__init__(queue, interval)
        self._directory = Path(directory)
        self._cyclic_queue: CyclicQueue[Path] = CyclicQueue()
        self._watcher_job: aio.Task | None = None
        self._filetype = filetype
        self._ready = aio.Event()
        self._logger = base_logger.getChild(f"FsResourceQueue({self._directory})")

    async def _worker(self):
        #  TODO: add filtering based on filetype
        while True:
            for file in filter(self._filetype, self._directory.iterdir()):
                if self._cyclic_queue.add_item(file):
                    self._logger.info(f"Adding {file}")
                self._ready.set()
            await aio.sleep(self._interval)

    async def setup(self):
        self._watcher_job = aio.create_task(self._worker())

    async def teardown(self):
        assert isinstance(self._watcher_job, aio.Task)
        self._watcher_job.cancel()

    async def next_resource(self) -> dict | None:
        await self._ready.wait()
        next_media = self._cyclic_queue.next_media()
        if not next_media:
            return None
        return {
            "payload": str(next_media),
            "display_time": time.time(),
        }
