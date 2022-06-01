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

videos = pd.read_json("/tiktok_data/Data/VideoMetadata.json",lines=True)

driver =  webdriver.Chrome("./chromedriver.exe")
api = TikTokCollector.CommentCollector(driver)
for url in videos['Url']:
    data = api.getStatisticsFromUrl(url)
    with open("/tiktok_data/Data/Comments.json","a") as file:
        for line in data:
            write_document_to_file(line,file)
    time.sleep(0.5)
driver.quit()