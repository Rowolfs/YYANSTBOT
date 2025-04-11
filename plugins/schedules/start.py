from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from plugins.schedules import plugin_title
from plugins.schedules.keyboards.main import MainKeyboardCommand

router = Router()


@router.message(F.text == plugin_title)
async def start_by_message(message: Message,state: FSMContext):
    await message.answer("Редактирование расписаний", reply_markup=MainKeyboardCommand().build_keyboard())

@router.callback_query(F.text == plugin_title)
async def start_by_callback(callback: CallbackQuery ,state: FSMContext):
    await callback.message.answer("Редактирование расписаний", reply_markup=MainKeyboardCommand().build_keyboard())






