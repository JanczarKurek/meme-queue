import asyncio as aio
from collections.abc import Awaitable, AsyncGenerator
import logging
import inspect
from pathlib import Path
import time
from typing import Callable, TypeVar, Iterable

from containers.cyclic_queue import CyclicQueue
from resource.resource_queue import ResourceQueueBack
from resource.resource_provider import TimeBasedResourceProvider

base_logger = logging.getLogger(__name__)
Filetype = Callable[[Path], bool | Awaitable[bool]]
true = lambda p: True

T = TypeVar("T")

async def afilter(pred: Callable[[T], bool | Awaitable[bool]], it: Iterable[T]) -> AsyncGenerator[T]:
    for e in it:
        result = pred(e)
        if inspect.isawaitable(result):
            result = await result
        else:
            await aio.sleep(0)
        if result:
            yield e


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
        while True:
            async for file in afilter(self._filetype, self._directory.iterdir()):
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
