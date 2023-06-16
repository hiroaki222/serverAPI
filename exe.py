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

weather = scraper.weather()
diagram = scraper.railway()
weather.update(diagram)
j = json.dumps(weather, indent=2, ensure_ascii=False )
print(j)