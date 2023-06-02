import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sqlite3

options = Options()
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)

id = 0

con = sqlite3.connect('detabase.db')
cur = con.cursor()
cur.execute('SELECT location FROM profiles WHERE id = ?', (id,))

driver.get(cur.fetchall()[0][0])

element = driver.find_element(By.XPATH, '//*[@id="yjw_pinpoint_today"]/table')
trs = element.find_elements(By.TAG_NAME, 'tr')

for i in trs:
    tds = i.find_elements(By.TAG_NAME, 'td')
    for j in tds:
        j = j.find_element(By.TAG_NAME, 'img')
        print(j.get_attribute('alt'))
#d = {3 * i - 3 : '' for i in range(1, 9)}
