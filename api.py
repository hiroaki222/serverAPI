import chromedriver_binary
import datetime
from flask import Flask, jsonify, render_template, request
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import scraper
import sqlite3

with open('config.json') as f:
    di = json.load(f)

def data():
    weather = scraper.weather()
    diagram = scraper.railway()
    news = scraper.news()
    weather.update(diagram)
    weather.update(news)
    return json.dumps(weather, indent=2, ensure_ascii=False )

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods = ['GET'])
def data():
    return jsonify(data())

@app.route('/detect', methods = ['PUT'])
def detect():
    
    rt = {'Status' : 'Success'}
    return jsonify(rt)

if __name__=='__main__':
    app.debug=True
    app.run(host=di['ip'], port=di['port'])