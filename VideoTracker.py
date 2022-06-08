import pandas as pd
from selenium import webdriver
import TikTokCollector
import json
import time
from datetime import datetime
from selenium.webdriver.chrome.options import Options
 


def write_document_to_file(document, file):
    json.dump(document, file)
    file.write("\n")
    file.flush()

videos = pd.read_json("Data/VideoMetadata.json",lines=True)

try:
    logs = pd.read_json("Data/VideoLogging.json",lines=True)
except:
    logs = pd.DataFrame(columns=["Url",'User',"UserId","ProfileBio","Followers","Following","LikeCount","CollectionDate","Status"])

options = Options()
options.headless = True
options.add_argument("--window-size=1024,768")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
driver =  webdriver.Chrome("/tiktok_data/MixedTiktokCollector/chromedriver",options=options)
api = TikTokCollector.VideoStatisticsCollector(driver)
newData=[]
today = datetime.now().strftime("%Y-%m-%d")
for url in videos['Url']:
    print(url)
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
print("Saving videos")
with open("Data/VideoLogging.json","a") as file:
    for line in newData:
        write_document_to_file(line,file)