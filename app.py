from flask import Flask, render_template, url_for
from test import scrap_link, get_month
from scrapper import Scrapper
from flask_apscheduler import APScheduler
from datetime import datetime
app = Flask(__name__)


scrapper = Scrapper()

websites_names = scrapper.get_webnames()

#scrapper.get_all_reports()
#scrapper.get_all_papers()
#scrapper.get_all_speeches()

scheduler = APScheduler()
scheduler.init_app(app)


@scheduler.task('cron', hour='*/4', id ='scrap')  # Runs every 6 hours
def scheduled_task():
    try: 
        scrapper.get_report_wb()
        scrapper.get_bis_ifcreports()
        scrapper.get_bis_bsbreports()
        scrapper.get_bis_cpmireports()
        scrapper.get_bis_cgfsreports()
        scrapper.get_report_fsb()
        scrapper.get_fem_reports()
        scrapper.get_imf_reports()
        scrapper.get_oecd_reports()
    except Exception as e:
        print(f'Error: {e}')
    print("Task executed.")

@app.route('/')
def main(): 
    return render_template('index.html', 
                           websites = scrapper.get_all_websites(), 
                           names = websites_names,
                           month = scrapper.get_month(),
                           zip= zip,
                           len = len,  
                           )



scheduler.start()
#print(scheduler.get_job(id='scrap'))
try:
    scheduler.run_job(id = 'scrap') #just uncomment for testing purposes. It will run the job now instead of the scheduled hour.
except Exception as e:
    print(f'Error: {e}') 
#print(scheduler.get_job(id='scrap'))

if __name__ == "__main__": 
    
    scheduler.start()
    print(scheduler.get_job(id='scrap'))
    scheduler.run_job(id = 'scrap') #just uncomment for testing purposes. It will run the job now instead of the scheduled hour. 
    print(scheduler.get_job(id='scrap'))
    app.run(debug=False)