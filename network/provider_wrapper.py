from resource.resource_queue import ResourceQueueBack
from resource.resource import Resource

import aiohttp

class HttpQueueBack(ResourceQueueBack):
    """Connects given provider with a queue"""
    def __init__(self, connection: aiohttp.client.ClientSession):
        self._connection = connection

    async def put(self, r: Resource):
        await self._connection.put(
            "/event",
            json=r.to_json()
        )
