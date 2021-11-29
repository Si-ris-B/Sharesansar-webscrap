import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def click_and_download(number):
    button = browser.find_element(By.XPATH,'//*[@id="btn_cpricehistory"]')
    button.click()

html = None
url = 'https://www.sharesansar.com/company/adbl'
selector = '#myTableCPriceHistory > tbody:nth-child(2) > tr:nth-child(1)'
delay = 20  # seconds

browser = webdriver.Firefox('/media/anon/Storage/Coding/Web Scrapping/geckodriver-v0.30.0-linux64/geckodriver')
browser.maximize_window()
browser.get(url)

try:
    # wait for button to be enabled
    WebDriverWait(browser, delay).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="btn_cpricehistory"]'))
    )
    button = browser.find_element(By.XPATH,'//*[@id="btn_cpricehistory"]')
    button.click()

    # wait for data to be loaded
    WebDriverWait(browser, delay).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )
except TimeoutException:
    print('Loading took too much time!')
else:
    html = browser.page_source

try:


finally:
    browser.quit()

if html:
    soup = BeautifulSoup(html, 'lxml')
    # raw_data = soup.select_one(selector).text
    # data = json.loads(raw_data)

    # import pprint
    # pprint.pprint(data)
    # soup = BeautifulSoup(html)
    with open("test1.txt", "w") as f:
        f.write(soup.prettify())