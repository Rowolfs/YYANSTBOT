from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from commandflow.commands.base import KeyboardCommand
from commandflow.core import QueueCommands
from config import get_db, logger 
logger.info("schedule_editor.py: модуль загружен")




queue1 = QueueCommands(queue=[("InputCommand",{"prompt": "Введите название расписания", "input_key": "schedule_name"}),("PrintHello",{})])
queue2 = QueueCommands(queue=[("SelectSchedule",{}),("PrintHello",{})])

@QueueCommands.register
class ScheduleEditorCommand(KeyboardCommand):

    def build_keyboard(self, **context):
        
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="Создать слот", callback_data=f"cf:{queue1.id}"))
        builder.row(InlineKeyboardButton(text="Изменить слот", callback_data=f"cf:{queue1.id}"))
        builder.row(InlineKeyboardButton(text="Удалить слот", callback_data=f"cf:{queue1.id}"))
        builder.row(InlineKeyboardButton(text="Выйти в редактор расписания", callback_data=f"start"))
        return builder.as_markup()