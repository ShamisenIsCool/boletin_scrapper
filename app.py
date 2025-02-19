from flask import Flask, render_template, url_for
from test import scrap_link, get_month
from scrapper import Scrapper
app = Flask(__name__)


scrapper = Scrapper()

websites_names = scrapper.get_webnames()
scrapper.get_imf_wp()
scrapper.get_speech_bis()
scrapper.get_speech_imf()


list = ['https://animepahe.ru/play/7808db84-55f1-f313-1019-e688b62574cf/0fe24c039b4704268808c8f71671f8a2c8c4eef9bb922acbdff9e3b96b1dd94e',
        'https://animepahe.ru/play/7808db84-55f1-f313-1019-e688b62574cf/0fe24c039b4704268808c8f71671f8a2c8c4eef9bb922acbdff9e3b96b1dd94e']

#list = scrap_link()

@app.route('/')
def main(): 
    return render_template('index.html', 
                           links = scrapper.get_all_websites(), 
                           names = websites_names,
                           month = scrapper.get_month(),
                           )