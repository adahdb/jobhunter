from scheduler.asyncio import Scheduler
import datetime
import Platsbanken
import db
import services
import telegramBot
import datetime as dt


async def init():
    services.scheduler = Scheduler()
    await tasks_init()


async def tasks_init():
    services.scheduler.daily(
        dt.time(hour=12, minute=00),
        get_and_send_daily_jobs
    )


async def get_and_send_daily_jobs():
    yesterday_date = datetime.date.today() - datetime.timedelta(days=1)
    formatted_yesterday = yesterday_date.strftime('%Y-%m-%dT00:00:00')

    print("Fetching daily jobs...")
    api_job_data = Platsbanken.getJobs(yesterday_date)
    db.save_jobs(api_job_data)

    print(f"Getting jobs from {yesterday_date}")
    jobs = db.get_jobs_by_fields("apaJ_2ja_LuF", "CaRE_1nn_cSU", formatted_yesterday)

    await telegramBot.send_jobs(jobs)