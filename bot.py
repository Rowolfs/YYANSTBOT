import asyncio
import importlib
import pkgutil
from aiogram import Bot, Dispatcher, Router
from config import TOKEN, engine, logger, Base, bot
from commandflow.router import router
from commandflow.commands.input import router as input_router




import sys
import os

# Добавляем корень проекта в sys.path, чтобы работали вложенные импорты
sys.path.append(os.path.abspath(os.path.dirname(__file__)))



Base.metadata.create_all(bind=engine)

from plugins.schedules.keyboards.schedule_editor import ScheduleEditorCommand
from plugins.schedules.keyboards.select_schedules import SelectSchedule

# Dispatcher
dp = Dispatcher()
dp.include_router(router)  # Подключаем маршрутизатор для состояний
dp.include_router(input_router) # Подключаем маршрутизатор для ввода текста



def import_all_routers(package_name: str) -> list[Router]:
    routers = []

    package = importlib.import_module(package_name)

    for _, name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        try:
            module = importlib.import_module(name)
            router = getattr(module, "router", None)
            if isinstance(router, Router):
                print(f"[✓] Подключен router из: {name}")
                routers.append(router)
        except Exception as e:
            print(f"[!] Ошибка импорта {name}: {e}")

    return routers


# Подключаем все router-ы из плагинов
for router in import_all_routers("plugins"):
    dp.include_router(router)

async def main():
    # Запускаем бота
    logger.info("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())