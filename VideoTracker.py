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

try:
    logs = pd.read_json("/tiktok_data/Data/VideoLogging.json",lines=True)
except:
    logs = pd.DataFrame(columns=["Url",'User',"UserId","ProfileBio","Followers","Following","LikeCount","CollectionDate","Status"])

while True:
    driver =  webdriver.Chrome("./chromedriver.exe")
    api = TikTokCollector.VideoStatisticsCollector(driver)
    newData=[]
    today = datetime.now().strftime("%Y-%m-%d")
    for url in videos['Url']:
        checked=False
        try:
            checked = (logs[logs['Url']==url].iloc[-1]["CollectionDate"] == today)
        except:
            pass
        if checked:
            continue
        data = api.getStatisticsFromUrl(url)
        newData.append(data)
        time.sleep(0.5)
    driver.quit()
    with open("/tiktok_data/Data/VideoLogging.json","a") as file:
        for line in newData:
            write_document_to_file(line,file)
    time.sleep(86400)