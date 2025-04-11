### commandflow/commands/base.py

from abc import ABC, abstractmethod
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext


class StepCommand(ABC):
    name = None
    wait_for_user_input = False

    async def __call__(self, message_or_callback, state: FSMContext, queue_id=None, **context):
        self.message = getattr(message_or_callback, 'message', message_or_callback)
        self.state = state
        self.queue_id = queue_id
        self.context = context

        await self.run(message_or_callback, state, **context)

        if queue_id is not None and not self.wait_for_user_input:
            await self.next()

    @abstractmethod
    async def run(self, message_or_callback, state: FSMContext, **context):
        pass

    async def next(self):
        from commandflow.core import QueueCommands
        await QueueCommands.next(self.message, self.state, self.queue_id, **self.context)


class KeyboardCommand(StepCommand, ABC):
    @abstractmethod
    def build_keyboard(self, **context):
        pass

    async def run(self, message: Message, state: FSMContext, **context):
        keyboard = self.build_keyboard(**context)
        self.context = context
        prompt = context.get("prompt")
        await message.answer(prompt, reply_markup=keyboard)
        await self.next()
