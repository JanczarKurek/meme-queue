import unittest

from containers.cyclic_queue import CyclicQueue


class CyclicQueueTest(unittest.TestCase):

    def setUp(self):
        self.queue: CyclicQueue[int] = CyclicQueue()

    def test_add_items(self):
        self.queue.add_item(1, CyclicQueue.ItemStatus.NORMAL)
        self.queue.add_item(2, CyclicQueue.ItemStatus.NORMAL)

        t = self.queue.next_media(), self.queue.next_media(), self.queue.next_media()
        self.assertEqual(t, (1, 2, 1))

    def test_add_new_items(self):
        self.queue.add_item(1)
        self.queue.add_item(2)

        t = self.queue.next_media(), self.queue.next_media()
        self.assertEqual(t, (2, 1))

    def test_add_mixed(self):
        self.queue.add_item(1)
        self.queue.add_item(2)
        t = self.queue.next_media()
        self.assertEqual(t, 2)

        self.queue.add_item(3)
        t = self.queue.next_media(), self.queue.next_media()
        self.assertEqual(t, (3, 1))

    def test_block(self):
        self.queue.add_item(1)
        self.queue.add_item(2)
        self.queue.block_media(2)

        t = self.queue.next_media(), self.queue.next_media()
        self.assertEqual(t, (1, 1))

    def test_request(self):
        self.queue.add_item(1)
        self.queue.request_media(5)

        t = self.queue.next_media(), self.queue.next_media(), self.queue.next_media()
        self.assertEqual(t, (5, 1, 1))


if __name__ == "__main__":
    unittest.main()
