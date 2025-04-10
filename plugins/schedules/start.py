from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from plugins.schedules import plugin_title
from plugins.schedules.keyboards.main import MainKeyboardCommand

router = Router()


@router.message(F.text == plugin_title)
async def start(message: Message,state: FSMContext):
    await message.answer("Привет", reply_markup=MainKeyboardCommand().build_keyboard())






