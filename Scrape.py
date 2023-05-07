import asyncio
from playwright.async_api import async_playwright
from time import time
from bs4 import BeautifulSoup
import re
import pandas as pd
from tqdm import tqdm
import os
from selenium import webdriver
import threading
import multiprocessing


url = "https://www.hltv.org/stats/players/matches/11893/zywoo"

headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
}

def scrape_pages(pages, skip=True):
    driver = webdriver.Firefox()
    for name in tqdm(pages):
        t = time()
        url = "https://www.hltv.org/stats/players/matches/" + name
        if not skip or name.replace("/","") not in os.listdir("../Final Project/scraped pages"):
            driver.get(url)
            html = driver.page_source
            with open("scraped pages/{}".format(name.replace("/","")),"w", encoding="utf-8") as f:
                f.write(html)
                f.close()
            print("Scraped {}, took {} seconds".format(name,time()-t))

async def scrape_names(playwright,):
    chromium = playwright.firefox # or "firefox" or "webkit".
    browser = await chromium.launch()
    page = await browser.new_page()
    url = "https://www.hltv.org/stats/players/"
    await page.goto(url)
    print("Going to player names")
    html = await page.content()
    with open("players_page.html", "w", encoding="utf-8") as f:
        f.write(html)
        f.close()
    await browser.close()

def chunks(lst, n): # n evenly sized chunks
    n = int(len(lst)/n)+1
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def main():
    n = 1
    pages = get_player_list("players_page.html")
    threads = [threading.Thread(target=scrape_pages, args=([subset])) for subset in chunks(pages,n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()




def get_player_list(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        bs = BeautifulSoup(f, features='lxml')
        rows = bs.find('table')
        pattern = r"/stats/players/(.*?)?\""
        return re.findall(pattern, str(rows))


main()