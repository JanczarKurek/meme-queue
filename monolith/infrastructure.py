"""Run all infrastructure on a single host"""
import asyncio as aio
from typing import Iterable

import aiohttp.web as web

from network.queue_wrapper import HTTPQueueWrapper
from resource.resource_queue import ResourceQueue
from resource.resource_provider import ResourceProvider


async def execute_infrastructure(queue: ResourceQueue, providers: Iterable[ResourceProvider]):
    http_queue = HTTPQueueWrapper(queue, "pomidor")
    app = web.Application()
    http_queue.apply_to_app(app, output_only=True)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 8080)
    await aio.gather(site.start(), *(provider.run() for provider in providers))
