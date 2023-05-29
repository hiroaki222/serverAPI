import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
#options.add_argument('--headless')
path = '/opt/google/chrome/google-chrome'
driver = webdriver.Chrome(executable_path=path, options=options)
driver.implicitly_wait(5)

driver.get('google.com')
element = driver.find_elements(By.TAG, 'h1')
print(element)
