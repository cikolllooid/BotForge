from aiogram import Bot, Dispatcher
import asyncio
from forRouters import router

bot = Bot(token='Tg bot token from @BotFather')
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

asyncio.run(main())