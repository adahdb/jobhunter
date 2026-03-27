import config
import services
import db
import telegramBot
import asyncio
import task_scheduler


async def main():
    db.init()
    await telegramBot.init()
    await task_scheduler.init()

    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
