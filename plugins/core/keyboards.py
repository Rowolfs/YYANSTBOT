import importlib
import pkgutil
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import Message, ReplyKeyboardMarkup
from plugins.core.models import ChatUserBase
from config import get_db


def main_menu(message: Message) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    db = next(get_db())

    # Add plugin buttons
    set_plugins_button(builder)

    # Admin-only button
    if message.chat.id != message.from_user.id:
        chat_user = db.query(ChatUserBase).filter(
            (ChatUserBase.user_id == message.from_user.id) &
            (ChatUserBase.chat_id == message.chat.id)
        ).first()
        if chat_user and chat_user.is_admin:
            builder.add(ReplyKeyboardButton(text="Администрирование"))

    return builder.as_markup(resize_keyboard=True)


def set_plugins_button(builder: ReplyKeyboardBuilder):
    """Динамически загружает названия плагинов как кнопки."""
    base_package = "plugins"

    for plugin_info in pkgutil.walk_packages([base_package], base_package + "."):
        if plugin_info.name == "plugins.core":
            continue
        if len(plugin_info.name.split(".")) != 2:
            continue
        try:
            module = importlib.import_module(plugin_info.name)
            plugin_name = getattr(module, "plugin_title", None)
            if plugin_name:
                builder.add(text=f"{plugin_name.capitalize()}")
        except Exception as e:
            print(f"Ошибка при загрузке плагина {plugin_info.name}: {e}")
            continue


def admin_menu(message: Message):
    builder = InlineKeyboardBuilder()
    db = next(get_db())
    chats_users = db.query(ChatUserBase).filter(message.chat.id == ChatUserBase.chat_id)
    builder.button(text="Добавить администратора Бота (только в этом чате)", callback_data="add")
    return builder.as_markup()
