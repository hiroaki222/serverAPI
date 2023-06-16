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

def flag(s):
    with open('data.json') as f:
        di = json.load(f)
    match s:
        case 'r':
            return di['flag']
        case 'w':
            di['flag'] = di['flag']  ^ 1
            with open('data.json', 'w') as f:
                json.dump(di, f, indent=2, ensure_ascii=False)
            return
    return di
di = flag('')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get():
    f = flag('r')
    
    rt = {"flag": f}
    return jsonify(rt)

@app.route('/detect', methods = ['POST'])
def detect():
    tmp = flag('r')
    if request.form['flag'] != str(flag('r')):
        flag('w')

    rt = {'Status' : 'Success'}
    return jsonify(rt)

if __name__=='__main__':
    app.debug=True
    app.run(host=di['ip'], port=di['port'])