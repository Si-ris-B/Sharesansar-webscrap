# importing the libraries

from bs4 import BeautifulSoup
import time
import requests


headers2 = {
"Connection": "keep-alive",
"DNT": "1",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Sec-Fetch-Site": "none",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Dest": "document",
"Referer": "https://www.sharesansar.com/",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

link = 'https://www.sharesansar.com/company/adbl#cpricehistory'

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

def readFromFile():
    with open("test1.txt") as f:
        soup = BeautifulSoup(f,'lxml')
        return soup

def find_table(soup):
    table = soup.find('table', { 'id': 'myTableCPriceHistory'})
    t1 = table.find("thead")
    # print(t1)
    # t2 = t1.find('tr')
    # print(t2)
    print([th.text.strip() for th in t1.find("tr").find_all("th")])
    
    return table

def get_all_rows(tb):
    table = tb.find('tbody')
    print([[td.text.strip() for td in tr.find_all("td")] for tr in table.find_all("tr")])

if __name__ == "__main__":
    # soup = get_soup(link, headers2)
    # print(soup.prettify())
    # download_webpage(link,headers2)

    soup = readFromFile()
    # # print(soup.prettify())
    tb = find_table(soup)
    get_all_rows(tb)