from flask import Flask, render_template, url_for
from test import scrap_link, get_month
from scrapper import Scrapper
from flask_apscheduler import APScheduler
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
    scrapper.get_all_reports()
    scrapper.get_all_papers()
    scrapper.get_all_speeches()    
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



if __name__ == "__main__": 
    
    scheduler.start()
    print(scheduler.get_job(id='scrap'))
    scheduler.run_job(id = 'scrap')
    print(scheduler.get_job(id='scrap'))
    app.run(debug=False)