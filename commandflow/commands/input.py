### commandflow/commands/input.py

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from commandflow.commands.base import StepCommand
from commandflow.core import QueueCommands
from config import logger

class InputStates(StatesGroup):
    input_text = State()


@QueueCommands.register
class InputCommand(StepCommand):
    wait_for_user_input = True
    async def run(self, message: Message, state: FSMContext, **context):
        try:
            prompt = context.get("prompt")
            input_key = context.get("input_key")
        except Exception as e:
            logger.error(f"Can't get data from context: {e}")
            return

        await message.answer(prompt)
        await state.set_data({
            "queue_id": self.queue_id,
            "input_key": input_key,
            "context": context
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

    
    await QueueCommands.next(message, state, queue_id, **context)
