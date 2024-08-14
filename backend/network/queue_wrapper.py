import json as js
import logging

from http import HTTPStatus
import aiohttp.web as web

from resource.resource import Resource
from resource.resource_queue import ResourceQueue


class HTTPQueueWrapper:
    """Implements queue that is available via http"""
    # TODO: Add validation to API.

    def __init__(self, resource_queue: ResourceQueue, api_prefix: str):
        self._logger = logging.getLogger(__name__ + f".HTTPQueueWrapper({api_prefix})")
        self._actual_queue = resource_queue
        self._api_prefix = api_prefix

    async def put_handler(self, request: web.Request) -> web.Response:
        body = js.loads(await request.read())
        try:
            resource = Resource.from_json(body)
        except TypeError as e:
            self._logger.error("Could not parse resource from the request.")
            return web.Response(status=HTTPStatus.BAD_REQUEST)
        await self._actual_queue.put(resource)
        return web.Response(status=HTTPStatus.OK)

    async def get_some_handler(self, request: web.Request) -> web.Response:
        if not (result:=[x.to_json() for x in await self._actual_queue.get_some()]):
            self._logger.warning("Empty result to be return, no events in queue.")
        return web.json_response(result)

    def apply_to_app(self, app: web.Application, output_only: bool):
        queue_app = web.Application()
        queue_app.add_routes([web.get("/someEvents", self.get_some_handler)])
        if not output_only:
            queue_app.add_routes([web.put("/event", self.put_handler)])
        app.add_subapp(f"/{self._api_prefix}", queue_app)
