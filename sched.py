import fsl_data_gen
import sales_data_gen
import services_data_gen
import B2B_commerce_gen
import approval_gen
import campaing_gen
import fundraising_gen
import lead_trending_gen
import social_gen
import subscription_gen
import fins_ido_wealth_gen
import fsc_wealth_gen
import fsc_wealth_cumulus_gen

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
def scheduled_B2B_commerce_gen():
    B2B_commerce_gen.run()

@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=13)
def scheduled_approval_gen():
    approval_gen.run()

@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=14)
def scheduled_campaing_gen():
    campaing_gen.run()

@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=15)
def scheduled_fundraising_gen():
    fundraising_gen.run()

@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=16)
def scheduled_lead_trending_gen():
    lead_trending_gen.run()

@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_social_gen():
    social_gen.run()

@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=18)
def scheduled_subscription_gen():
    subscription_gen.run()

@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=19)
def scheduled_fins_ido_wealth_gen():
    fins_ido_wealth_gen.run()

@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=20)
def scheduled_fsc_wealth_gen():
    fsc_wealth_gen.run()

@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=21)
def scheduled_fsc_wealth_cumulus_gen():
    fsc_wealth_cumulus_gen.run()
    
scheduler.start()
