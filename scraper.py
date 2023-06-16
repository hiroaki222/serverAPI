
import chromedriver_binary
import datetime
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sqlite3

def weather():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    id = 0

    con = sqlite3.connect('detabase.db')
    cur = con.cursor()
    cur.execute('SELECT location FROM profiles WHERE id = ?', (id,))

    driver.get(cur.fetchall()[0][0])
    print('done!')
    update = driver.find_element(By.XPATH, '//*[@id="addpsnl"]/p[2]').text
    weather = [[driver.find_element(By.XPATH, f'//*[@id="yjw_pinpoint_today"]/table/tbody/tr[{i}]/td[{j}]/small').text for j in range(2, 10)] for i in range(2, 7)]

    tmp = [re.sub(r'\n\d+', '', item) for item in weather[4]]
    tmp1 = [re.search(r'\n(\d+)', item).group(1) for item in weather[4] if re.search(r'\n(\d+)', item)]
    weather.pop(4)
    weather.append(tmp)
    weather.append(tmp1)

    umbrella = []
    umbrella.append(driver.find_element(By.XPATH, '//*[@id="index-01"]/dl[2]/dd/p[1]/span').get_attribute("textContent"))
    umbrella.append(driver.find_element(By.XPATH, '//*[@id="index-01"]/dl[2]/dd/p[2]').text)

    tmp = []
    tmp.append(update)
    tmp.append(weather)
    tmp.append(umbrella)

    export = {
        'update' : update.replace('\u3000', ' '),
        'weather' : weather[0],
        'temperature' : weather[1],
        'humidity' : weather[2],
        'precipitation' : weather[3],
        'direction' : weather[4],
        'speed' : weather[5],
        'umbrella' : umbrella
    }

    return export

def railway():
    dt = datetime.datetime.now()
    url = 'https://transit.yahoo.co.jp/timetable/25514/1590?ym='
    url += dt.strftime('%Y%m') + '&d=' + dt.strftime('%d') + '&hh=' + dt.strftime('%H') + '&q=草津(滋賀県)'

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    return url