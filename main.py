import logging
import asyncio
import sys
from aiogram import Bot, Dispatcher, F

from config import BOT_TOKEN

from app.handlers import router
from app.database.models import async_main

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


dp = Dispatcher()
bot = Bot(BOT_TOKEN)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Добавляем роутер ОДИН РАЗ, до цикла
dp.include_router(router)


async def main():
    while True:
        try:
            await async_main()
            print("База данных подключена")
            logging.info("Бот запускается")
            await dp.start_polling(bot, skip_updates=True)
        except Exception as e:
            logging.error(f"Ошибка {e}")
            logging.info("Перезапуск")
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")