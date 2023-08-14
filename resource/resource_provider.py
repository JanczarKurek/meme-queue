import abc
import asyncio

from resource.resource import Resource
from resource.resource_queue import ResourceQueue


class ResourceProvider(abc.ABC):
    """Basic resource provider"""

    RESOURCE_TAG: str = "None"

    def __init__(self, queue: ResourceQueue):
        self._queue = queue

    async def put_resource(self, **kwargs):
        await self._queue.put(Resource(**kwargs, resource_tag=self.RESOURCE_TAG))
    
    @abc.abstractmethod
    async def run(self):
        """Main loop of ResourceProvider"""


class TimeBasedResourceProvider(ResourceProvider):
    """Resource provider that puts a resource in a regular manner"""

    def __init__(self, queue: ResourceQueue, interval: float):
        self._interval = interval
        super().__init__(queue)
    
    async def setup(self):
        pass

    async def teardown(self):
        pass

    @abc.abstractmethod
    async def next_resource(self) -> dict | None:
        pass

    async def run(self):
        await self.setup()
        while True:
            await asyncio.sleep(self._interval)
            if next_resource:=await self.next_resource():
                await self.put_resource(**next_resource)
        await self.teardown()
