import Platsbanken
import task_scheduler
import datetime

yesterday_date = datetime.date.today() - datetime.timedelta(days=1)


def main():
    jobs=Platsbanken.getJobs(yesterday_date)
    print(len(jobs))


main()