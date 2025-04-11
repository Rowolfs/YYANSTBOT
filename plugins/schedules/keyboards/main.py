from plugins.schedules.commands.crud_schedule import PrintHello
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from commandflow.commands.base import KeyboardCommand
from commandflow.core import QueueCommands


queue1 = QueueCommands(queue=[("InputCommand",{"prompt": "Введите название расписания", "input_key": "schedule_name"}),("PrintHello",{})])
queue2 = QueueCommands(queue=[("select_schedules",{}),("PrintHello",{})])

@QueueCommands.register
class MainKeyboardCommand(KeyboardCommand):

    def build_keyboard(self, **context):
        
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="Создать Расписание", callback_data=f"cf:{queue1.id}"))
        builder.row(InlineKeyboardButton(text="Выбрать Расписание", callback_data=f"cf:{queue1.id}"))
        builder.row(InlineKeyboardButton(text="Удалить Расписание", callback_data=f"cf:{queue1.id}"))
        builder.row(InlineKeyboardButton(text="Выйти в главное Меню", callback_data=f"start"))
        return builder.as_markup()