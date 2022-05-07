# importing the libraries

from bs4 import BeautifulSoup
import requests
import csv
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import random

def get_soup(url, header):

    html_content = requests.get(url,headers = header).text
    # Parse the html content
    soup = BeautifulSoup(html_content, "html")
    return soup

def download_webpage(url, header):

    html_content = requests.get(url,headers = header).content
    soup = BeautifulSoup(html_content)
    with open("test.txt", "w") as f:
        f.write(soup.prettify())

def readFromFile(filename):
    with open(filename) as f:
        soup = BeautifulSoup(f,'lxml')
        return soup


def get_headers(table):
    t1 = table.find("thead")
    return [th.text.strip() for th in t1.find("tr").find_all("th")]
 

def get_all_rows(tb):
    table = tb.find('tbody')
    return [[td.text.strip() for td in tr.find_all("td")] for tr in table.find_all("tr")]

    from selenium.webdriver.common.by import By

def click_and_download(number,delay, table_list, browser):

    if number > 5:
        i = 4
    else:
        i = number

    xpath1 = f'/html/body/div[2]/div/section[2]/div[3]/div/div/div/div[2]/div/div[1]/div[2]/div/div[8]/div/div/div[5]/span/a[{i}]'
    button = browser.find_element(By.XPATH,xpath1)
    
    button.click()

    WebDriverWait(browser, delay).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )
    time.sleep(random.randint(5,10))
    html = browser.page_source
    table_list.append(get_table(html))

def find_table(soup):
    table = soup.find('table', { 'id': 'myTableCPriceHistory'})
    return table

def get_table(html,number=1):
    if html:
        soup = BeautifulSoup(html, 'lxml')        
        # with open(f"adbl-{number}.txt", "w") as f:
        #     f.write(soup.prettify())
        return find_table(soup)

def get_stock_table(company_symbol,delay=10):
    html = None
    url = f'https://www.sharesansar.com/company/{company_symbol}'
    global selector
    selector = '#myTableCPriceHistory > tbody:nth-child(2) > tr:nth-child(1)'
    delay = delay  # seconds
    table_list = []

    browser = webdriver.Firefox(executable_path='geckodriver-v0.30.0-linux64/geckodriver') #path to geckodriver

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

        select1 = select.Select(browser.find_element(By.CSS_SELECTOR,'#myTableCPriceHistory_length > label:nth-child(1) > select:nth-child(1)'))
        select1.select_by_visible_text("50")

        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        time.sleep(5)
        html = browser.page_source
        table_list.append(get_table(html))
    except TimeoutException:
        print('Loading took too much time!')
    

    for i in range(2,51): # Instead of 5, Put a number of the page in table till which you want to extract table
        try:
            click_and_download(i,delay, table_list, browser)
        except TimeoutException:
            print('Loading took too much time!')
            break


    browser.quit()

    headers = get_headers(table_list[0])

    return headers, table_list

def save_table_to_csv(csvname, table_list, headers):
    with open(csvname,'w') as c:
        csv_writer = csv.writer(c, delimiter=',', quotechar='"', 
        quoting=csv.QUOTE_MINIMAL)
        
        csv_writer.writerow(headers)

        for table in table_list:

            rowlist = get_all_rows(table)
            for row in rowlist:
                csv_writer.writerow(row)

if __name__ == "__main__":
    
    company_symbol = 'nabil'

    headers, table = get_stock_table(company_symbol,5)
    
    save_table_to_csv(f'{company_symbol}.csv', table, headers)
