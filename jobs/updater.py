from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_api,getting_btc_data,Telegram_data,show_count,update_token,Place_positional_order,create_row_14min,strategy_5
from pytz import utc
from apscheduler.triggers.cron import CronTrigger

def start():
	scheduler = BackgroundScheduler()
	scheduler.configure(timezone=utc)
	scheduler.add_job(create_row_14min, 'interval',  minutes=14)
	# scheduler.add_job(show_count, 'interval',  minutes=5)
	# scheduler.add_job(schedule_api, 'interval', minutes=15)
	# scheduler.add_job(clean_daily_db, 'interval', minutes=1)
	
	scheduler.add_job(update_token, 'interval',  minutes=297)
	scheduler.add_job(strategy_5, 'interval',  minutes=15)
	# scheduler.add_job(Place_positional_order, 'interval',  seconds=3)
	
	# scheduler.add_job(Telegram_data, 'interval', minutes=1)
	# scheduler.add_job(clean_daily_db,  CronTrigger.from_crontab('* 10 * * *'))
	scheduler.start()
