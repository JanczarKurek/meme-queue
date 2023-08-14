import asyncio

from monolith.infrastructure import execute_infrastructure
from resource.resource_queue import SimpleResourceQueue
from fs_resource_provider import FsResourceProvider

if __name__ == "__main__":
    queue = SimpleResourceQueue(10)
    asyncio.run(execute_infrastructure(queue, (FsResourceProvider(queue, 2., "/home/janczarknurek/dupa"),)))
    print(queue._content)
