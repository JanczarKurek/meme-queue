import abc
import asyncio

from resource.resource import Resource
from resource.resource_queue import ResourceQueueBack


class ResourceProvider(abc.ABC):
    """Basic resource provider"""

    RESOURCE_TAG: str = "None"

    def __init__(self, queue: ResourceQueueBack):
        self._queue = queue

    async def put_resource(self, **kwargs):
        await self._queue.put(Resource(**kwargs, resource_tag=self.RESOURCE_TAG))
    
    @abc.abstractmethod
    async def run(self):
        """Main loop of ResourceProvider"""


class TimeBasedResourceProvider(ResourceProvider):
    """Resource provider that puts a resource in a regular manner"""

    def __init__(self, queue: ResourceQueueBack, interval: float, startup_delay: float = 0.):
        self._interval = interval
        self._startup_delay = startup_delay
        super().__init__(queue)
    
    async def setup(self):
        pass

    async def teardown(self):
        pass

    async def run(self):
        await asyncio.gather(self.setup(), asyncio.sleep(self._startup_delay))
        while True:
            if next_resource:=await self.next_resource():
                await self.put_resource(**next_resource)
            else:
                await self.teardown()
                return
            await asyncio.sleep(self._interval)
