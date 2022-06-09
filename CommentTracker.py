import pandas as pd
from selenium import webdriver
import TikTokCollector
import json
import time
from datetime import datetime


def write_document_to_file(document, file):
    json.dump(document, file)
    file.write("\n")
    file.flush()

videos = pd.read_json("Data/VideoMetadata.json",lines=True)

opts = webdriver.ChromeOptions()
opts.add_argument("--window-size=1024,768")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--no-sandbox")
driver =  webdriver.Chrome("chromedriver.exe",options=opts)

api = TikTokCollector.CommentCollector(driver)
i = 0
for url in videos['Url']:
    data = api.getStatisticsFromUrl(url)
    print(len(data), "comments collected from", url)
    i += 1
    if i == 2:
        break
    with open("Data/Comments.json","a") as file:
        for line in data:
            write_document_to_file(line,file)
    time.sleep(0.5)
driver.quit()