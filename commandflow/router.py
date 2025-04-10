### commandflow/router.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from commandflow.core import QueueCommands

router = Router()

@router.callback_query(F.data.startswith("cf:"))
async def commandflow_callback(callback: CallbackQuery, state: FSMContext):
    # Разбиваем callback_data на части
    parts = callback.data.split(":", 2)
    
    # Проверка на корректность данных
    if len(parts) < 2:
        await callback.answer("Неверный формат callback_data", show_alert=True)
        return

    target = parts[1]  # Команда или queue_id
    raw_context = parts[2] if len(parts) == 3 else ""  # Контекст, если он есть
    context = {}

    # Парсим контекст, если он есть
    for pair in raw_context.split(","):
        if "=" in pair:
            key, value = pair.split("=", 1)
            context[key] = value


    context["from_user_id"] = callback.from_user.id

    # Если target — это queue_id, продолжаем очередь
    if target.isdigit():
        queue_id = int(target)
        await QueueCommands.set_active(callback.message, state, queue_id, **context)
    else:
        # Ищем команду по имени (target) в реестре команд
        command = QueueCommands.command_registry.get(target)
        if command:
            await command(callback, state, queue_id=None, **context)
        else:
            await callback.answer("Команда не найдена", show_alert=True)
