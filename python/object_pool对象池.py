import queue


class ObjectPool(object):
    """对象池"""
    def __init__(self, maxsize=0):
        self.active_queue = queue.Queue(maxsize=maxsize)  # 活跃区
        self.inactive_queue = queue.Queue()  # 闲置区

    def get(self, timeout=1):
        """从闲置区获取一个对象，并移入活跃区"""
        if self.__len__() == 0:
            return None
        try:
            instance = self.inactive_queue.get(timeout=timeout)
        except queue.Empty:
            return None
        self.active_queue.put_nowait(instance)
        return instance

    def put(self, instance):
        """存储一个对象进闲置区， 如其已在活跃区则移除"""
        try:
            self.inactive_queue.put_nowait(instance)
        except queue.Full:
            # 对象池满了，丢弃对象，不作处理
            pass
        if instance in self.active_pool:
            self.active_pool.remove(instance)

    def clear(self):
        self.clear_active_pool()
        self.clear_inactive_pool()

    def clear_active_pool(self):
        self.active_pool.clear()

    def clear_inactive_pool(self):
        self.inactive_pool.clear()

    def __len__(self):
        return self.inactive_queue.qsize()

    @property
    def active_pool(self):
        """:return: deque 所有活跃区中的元素"""
        return self.active_queue.queue

    @property
    def inactive_pool(self):
        """:return: deque 所有闲置区中的元素"""
        return self.inactive_queue.queue


if __name__ == '__main__':

    pool = ObjectPool()
    # 放一个元素进对象池
    pool.put("1")
    # 从对象池中取一个元素
    obj = pool.get()
