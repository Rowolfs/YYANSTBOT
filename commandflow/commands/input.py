### commandflow/commands/input.py

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from commandflow.commands.base import StepCommand


class InputStates(StatesGroup):
    input_text = State()


class InputCommand(StepCommand):
    def __init__(self, prompt: str, input_key: str = "input"):
        self.prompt = prompt
        self.input_key = input_key

    async def run(self, message: Message, state: FSMContext, **context):
        await message.answer(self.prompt)
        await state.set_data({
            "queue_id": self.queue_id,
            "input_key": self.input_key,
            "context": self.context
        })
        await state.set_state(InputStates.input_text)


# Хендлер, который нужно подключить в твоём роутере отдельно
from aiogram import Router

router = Router()

@router.message(InputStates.input_text)
async def handle_input_text(message: Message, state: FSMContext):
    data = await state.get_data()
    queue_id = data.get("queue_id")
    input_key = data.get("input_key", "input")
    context = data.get("context", {})

    context[input_key] = message.text
    await state.clear()

    from commandflow.core import QueueCommands
    await QueueCommands.next(message, state, queue_id, **context)
