### commandflow/core.py
from commandflow.storage import storage
import copy
import random
import asyncio

class QueueCommands:
    queues = {}
    command_registry = {}

    def __init__(self, queue=None):
        self.id = len(QueueCommands.queues)
        QueueCommands.queues[self.id] = self
        self.queue = queue if queue is not None else []
        self.cursor = 0
        self.context = {}
        self.size = len(self.queue)
    @staticmethod
    async def set_active(message, state, queue_id: int,**kwargs):
        queue =  await QueueCommands.get(queue_id)
        queue = copy.deepcopy(queue)
        queue.id = random.randint(0, 1000000)
        await storage.save(queue.id, queue.to_dict())
        await queue.next_by_instance(message, state, **kwargs)
        return queue

    @staticmethod
    async def get(id):
        data = await storage.load(id)
        if data:
            return QueueCommands.from_dict(data)
        else:
            queue = QueueCommands.queues.get(id)
            if queue:
                return queue
        return None
    
    @staticmethod
    async def repeat(message, state, queue_id: int, **kwargs):
        queue = await QueueCommands.get(queue_id)
        if queue is None:
            return
        queue.cursor -= 1
        await queue.next_by_instance(message, state, **kwargs)

    async def next_by_instance(self, message, state, **kwargs):
        if self.cursor >= self.size:
            await storage.delete(self.id)
            return

        command_func, command_args = self.queue[self.cursor]


        self.cursor += 1
        merged_args = {**command_args, **kwargs}
        self.context = {**self.context, **merged_args}
        await storage.save(self.id, self.to_dict())
        command = QueueCommands.command_registry.get(command_func)
        await command(message, state, self.id, **self.context)

    @classmethod
    async def next(cls, message, state, queue_id: int, **kwargs):
        queue = await cls.get(queue_id)
        if queue is None:
            return
        await queue.next_by_instance(message, state, **kwargs)

    def get_queue(self):
        return self.queue

    def to_dict(self):
        return {
            "id": self.id,
            "queue": [
                (func.__class__.__name__, args) for func, args in self.queue
            ],
            "cursor": self.cursor,
            "context": self.context,
            "size": self.size
        }

    @classmethod
    def from_dict(cls, data):
        queue = [
            (cls.command_registry[name], args) for name, args in data["queue"]
        ]
        obj = cls(queue=queue)
        obj.id = data["id"]
        obj.cursor = data["cursor"]
        obj.context = data["context"]
        obj.size = data["size"]
        return obj

    @classmethod
    def register(cls, command_cls):
        cls.command_registry[command_cls.__name__] = command_cls()
        return command_cls
