import asyncio

from core import (
    bot,
    dp,
    setup_routers
)

# Run the bot
async def main() -> None:
    setup_routers(dp=dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
          