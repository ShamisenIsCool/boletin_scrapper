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


@scheduler.task('cron', hour='*/4', id ='scrap')  # Runs every 3 hours
def scheduled_task(scrapper = scrapper):
    while True: 
        scrapper.clear_websites() #So each time the schedule is executed we dont get duplicated websites.
        scrapper.get_all_reports()
        scrapper.get_all_papers()
        scrapper.get_all_speeches()
    
        if scrapper.verify_integrity(): 
            #scrapper.get_wp_wb()
            print("Task executed.")
            return 
        else: 
            continue


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
print(scheduler.get_job(id='scrap'))

try:
    scheduler.run_job(id = 'scrap') #just uncomment for testing purposes. It will run the job now instead of the scheduled hour.
except Exception as e:
    print(f'Error: {e}') 



if __name__ == "__main__": 
    
    #scheduler.start()
    #print(scheduler.get_job(id='scrap'))
    #scheduler.run_job(id = 'scrap') #just uncomment for testing purposes. It will run the job now instead of the scheduled hour. 
    app.run(debug=False)
    pass