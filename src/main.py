import config
import services
import db
import telegramBot
import asyncio
import task_scheduler


async def main():
    db.init()
    print("DB Init")
    await telegramBot.init()
    print("TelegramBot Init")
    await task_scheduler.init()
    print("Task Scheduler Init")

    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
