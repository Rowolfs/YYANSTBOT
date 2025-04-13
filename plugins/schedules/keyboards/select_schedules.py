from commandflow.commands.base import KeyboardCommand
from commandflow.core import QueueCommands
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from config import get_db, logger
from plugins.schedules.models import ScheduleBase, UserScheduleBase
from plugins.schedules import plugin_title



queue1 = QueueCommands(queue=[("PrintHello",{})])


@QueueCommands.register
class SelectSchedule(KeyboardCommand):
    name = "select_schedules"

    def build_keyboard(self, **context):
        builder = InlineKeyboardBuilder()
        db = next(get_db())
        user_id = context.get("user_id")
        schedules = db.query(ScheduleBase).join(UserScheduleBase).filter(
            UserScheduleBase.user_id == user_id
        ).all()

        for schedule in schedules:
            button = InlineKeyboardButton(
                text=schedule.name,
                callback_data=f"cf:{queue1.id}:{schedule.id}"
            )
            builder.add(button)
        
        builder.row(InlineKeyboardButton(text="Назад", callback_data=f"{plugin_title}"))

        return super().build_keyboard(**context)