from flask import Flask, render_template, url_for
from test import scrap_link, get_month
from scrapper import Scrapper
app = Flask(__name__)


scrapper = Scrapper()

websites_names = scrapper.get_webnames()
#scrapper.get_imf_wp()
scrapper.get_speech_bis()
#scrapper.get_speech_imf()
#scrapper.get_speech_fsb()
#scrapper.get_basel_speeches()
#scrapper.get_bisManagement_speeches()
#scrapper.get_speech_imf()
#scrapper.get_fem_reports()
#list = scrap_link()

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