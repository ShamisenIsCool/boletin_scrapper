from flask import Flask, render_template, url_for
from test import scrap_link, get_month
from scrapper import Scrapper
app = Flask(__name__)


scrapper = Scrapper()

websites_names = scrapper.get_webnames()

#scrapper.get_all_papers()
#scrapper.get_all_reports()
scrapper.get_all_speeches()

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
    app.run(debug=False)