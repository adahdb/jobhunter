from scheduler.asyncio import Scheduler
import datetime
import Platsbanken
import db  # import the db module so we can call its functions
import services
import telegramBot


async def init():
    services.scheduler = Scheduler()
    await tasks_init()


async def tasks_init():
    services.scheduler.daily(
        datetime.time(hour=00, minute=34),
        get_and_send_daily_jobs  # no parentheses — pass the function reference
    )


async def get_and_send_daily_jobs():
    print("Fetching daily jobs...")
    api_job_data = Platsbanken.getJobs()
    db.save_jobs(api_job_data)

    yesterday_date = datetime.date.today() - datetime.timedelta(days=1)
    formatted_yesterday = yesterday_date.strftime('%Y-%m-%dT00:00:00')

    jobs = db.get_jobs_by_fields("apaJ_2ja_LuF", "CaRE_1nn_cSU", formatted_yesterday)

    await telegramBot.send_jobs(jobs)