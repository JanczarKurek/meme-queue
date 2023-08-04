import abc
from collections import deque

from resource import Resource


class ResourceQueue(abc.ABC):
    
    @abc.abstractmethod
    async def get_some(self) -> list[Resource]:
        """Returns an unspecified amount of Resources"""

    async def put(self, r: Resource):
        """Inserts resource into queue"""


class SimpleResourceQueue(ResourceQueue):

    def __init__(self, max_size: int):
        self._content: deque[Resource] = deque(maxlen=max_size)
    
    async def get_some(self) -> list[Resource]:
        ret = list(self._content)
        self._content.clear()
        return ret
    
    async def put(self, r: Resource):
        self._content.append(r)
