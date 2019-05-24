import fsl_data_gen
import sales_data_gen
import services_data_gen
import B2B_commerce_gen

from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=9)
def scheduled_sales_data_gen():
    sales_data_gen.run()

@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=10)
def scheduled_services_data_gen():
    services_data_gen.run()

@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=11)
def scheduled_fsl_data_gen():
    fsl_data_gen.run()

@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=12)
def scheduled_b2b_commerce_data_gen():
    B2B_commerce_gen.run()

scheduler.start()
