import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from revue.scripts.mail import generate_all_mail_files

scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


def schedule_cron_jobs():
    scheduler.add_job(
        func=generate_all_mail_files,
        trigger=IntervalTrigger(seconds=2),
        id='generate_mail_lists',
        name='Generate mail lists every minute',
        replace_existing=True)
