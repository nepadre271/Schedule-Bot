import asyncio
from config import dp, bot, router
from handlers import setup_handlers
from utils.db import init_db

setup_handlers(router)
init_db()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
