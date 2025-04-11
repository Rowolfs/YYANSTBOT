
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F, Router
from plugins.core.models import user_registration, chat_registration, chat_user_registration
from plugins.core.keyboards import main_menu, admin_menu
from config import bot

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    user_registration(message.from_user.id,message.from_user.full_name,message.from_user.username)
    if(message.chat.id != message.from_user.id):
        chat_registration(message.chat.id,message.chat.full_name)
        admins = await bot.get_chat_administrators(message.chat.id)
        admin_ids = [admins[i].user.id for i in range(len(admins))]
        if(message.from_user.id in admin_ids):
            chat_user_registration(chatId=message.chat.id,userId=message.from_user.id,isAdmin=True)
        else:
            chat_user_registration(chatId=message.chat.id,userId=message.from_user.id,isAdmin=False)
        await message.answer("Приветсвую", reply_markup=main_menu(message))
    await message.answer("Приветсвую", reply_markup=main_menu(message))
        
@router.callback_query(F.data == "start")
async def start_callback(callback: CallbackQuery):
    await callback.message.answer("Приветсвую", reply_markup=main_menu(callback.message))


@router.message(F.text == "Администрирование")
async def start_admin_menu(message: Message):
    await message.answer("admin menu", reply_markup=admin_menu(message))