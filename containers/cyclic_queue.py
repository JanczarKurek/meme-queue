from collections import deque
from enum import Enum
from typing import Generic, TypeVar


Item = TypeVar("Item")


class CyclicQueue(Generic[Item]):

    class ItemStatus(Enum):
        NEW = 'NEW'
        NORMAL = 'NORMAL'
        PENDING = 'PENDING'
        RETRACTED = 'RETRACTED'
        SPECIAL = 'SPECIAL'

    BAD_STATUSES = [ItemStatus.PENDING, ItemStatus.RETRACTED]

    def __init__(self):
        self._items: dict[Item, CyclicQueue.ItemStatus] = {}
        self._item_queue: deque[Item] = deque()
        self._pending_request = None
        self._already_returned = []

    def add_item(self, item: Item, status: ItemStatus = ItemStatus.NEW):
        if item not in self._items.keys():
            self._items[item] = status
            if status == self.ItemStatus.NEW:
                self._item_queue.append(item)
            elif status not in self.BAD_STATUSES:
                self._item_queue.appendleft(item)

    def _change_status(self, item: Item, status: ItemStatus):
        self._items[item] = status

    def block_media(self, meme_path: Item):
        self._change_status(meme_path, CyclicQueue.ItemStatus.PENDING)

    def request_media(self, media_path: Item):
        # This meme will be displayed regardless of a current queue
        # It won't show in a queue
        self._pending_request = media_path

    def _remember(self, item):
        self._already_returned.append(item)

    def next_media(self) -> Item | None:
        if self._pending_request:
            result = self._pending_request
            self._pending_request = None
            return result
        while True:
            if not self._item_queue:
                return None
            item = self._item_queue.pop()
            if self._items[item] in self.BAD_STATUSES:
                continue
            break
        self._change_status(item, CyclicQueue.ItemStatus.NORMAL)
        self._remember(item)
        self._item_queue.appendleft(item)
        return item

    def get_last_media(self, cnt: int):
        return self._already_returned[-cnt:]

    @property
    def items(self):
        return list(self._items.values())
