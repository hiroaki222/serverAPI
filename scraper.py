
import chromedriver_binary
import datetime
import json
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
    id = 0

    con = sqlite3.connect('detabase.db')
    cur = con.cursor()
    cur.execute('SELECT station FROM profiles WHERE id = ?', (id,))

    dt = datetime.datetime.now()
    url = cur.fetchall()[0][0]
    url += dt.strftime('%Y%m') + '&d=' + dt.strftime('%d') + '&hh=' + dt.strftime('%H')

    options = Options()
    #options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    driver.get(url)

    trs = driver.find_element(By.XPATH, '//*[@id="mdStaLineDia"]/div[2]/table[1]')
    trs = trs.find_elements(By.TAG_NAME, "tr")
    mm = [int(re.search(r"\d+", trs[1].get_attribute('id')).group()), int(re.search(r"\d+", trs[len(trs) - 1].get_attribute('id')).group())]

    if int(dt.strftime('%H')) < mm[0]:
        st = [mm[0], 2]
    elif int(dt.strftime('%H')) > mm[1]:
        st = [mm[1], 1]
    else:
        st = [int(dt.strftime('%H')), 2]

    diagram = {f'{st[0]}' : {}}
    for h in range(st[1]):
        lis = driver.find_element(By.XPATH, f'//*[@id="hh_{st[0]}"]/td[2]/ul')
        lis = lis.find_elements(By.TAG_NAME, 'li')

        dls = [driver.find_element(By.XPATH, f'//*[@id="hh_{st[0]}"]/td[2]/ul/li[{i}]/a/dl') for i in range(1, len(lis) + 1)]

        tmp = {}
        for i in dls:
            dds = i.find_elements(By.TAG_NAME, 'dd')
            tmpDict = {}
            for j in dds:
                if j.text.find('[') != -1:
                    temp = re.sub(r"\[|\]", "", j.text)
                    tmpDict["type"] = f'{temp}'
                else:
                    tmpDict["for"] = f"{j.text}"
                tmp[f'{re.sub(r"●", "", i.find_element(By.TAG_NAME, "dt").text)}'] = tmpDict

        diagram[f"{st[0]}"] = tmp
        st[0] += 1
    diagram = {"diagram" : diagram}
    return diagram

railway()