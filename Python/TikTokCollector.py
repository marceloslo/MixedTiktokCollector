import selenium
import re
import pickle
from datetime import datetime, timedelta
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth

def formatDate(date):
    publication_date = date
    if 'd' in date:
        value = int(re.search(r'\d+', publication_date).group())
        date_ago = (datetime.now() - timedelta(days=value)).date() 
        publication_date = date_ago.strftime("%Y-%m-%d")
    elif 'w' in date:
        value = 7*int(re.search(r'\d+', publication_date).group())
        date_ago = (datetime.now() - timedelta(days=value)).date() 
        publication_date = date_ago.strftime("%Y-%m-%d")
    elif 'ago' in date:
        publication_date = datetime.now().strftime("%Y-%m-%d")
    elif not publication_date:
        publication_date="2000-01-01"
    else:
        try:
            publication_date = datetime.strptime(publication_date,"%Y-%m-%d")
            publication_date = publication_date.strftime("%Y-%m-%d")
        except:
            publication_date = datetime.now().strftime("%Y")+"-"+publication_date
    return publication_date

class TikTokCollector:
    def __init__(self,driver):
        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        self.driver=driver
        self.url=""

    #url deve ser a url de um video no formato https://www.tiktok.com/@user/video/id para o coletor de video
    #ou https://www.tiktok.com/@user para o coletor de perfis
    def setUrl(self,url):
        self.url=url
        self.driver.get(url)

    #retorna dicionario com todas estatisticas visiveis do local analisado
    def getStatistics(self):
        return {}  

    #retorna dicionario com todas estatisticas visiveis do video da url dada
    def getStatisticsFromUrl(self,url):
        self.setUrl(url)
        return self.getStatistics()

class VideoStatisticsCollector(TikTokCollector):
    def __init__(self,driver):
        super().__init__(driver)

    #status 0=off, 1=on
    def getStatistics(self):
        if not self.__videoExists():
            stats = {"Url":self.url,'User':"","UserId":"","Description":"","LikeCount":"","CommentCount":"","SharesCount":"","PublicationDate":"","CollectionDate":datetime.now().strftime("%Y-%m-%d"),"Status":0}
            return stats
        stats = {}
        stats['Url'] = self.url
        stats['User'] = self.__getUser()
        stats['UserId'] = self.__getUserId()
        stats['Description'] = self.__getDescription()
        stats['LikeCount'] = self.__getLikes()
        stats['CommentCount']=self.__getCommentCount()
        stats['SharesCount']=self.__getShares()
        stats["PublicationDate"]=self.__getPublicationDate()
        stats["CollectionDate"] = datetime.now().strftime("%Y-%m-%d")
        stats['Status'] = 1
        return stats

    def getMetadata(self):
        data = self.getStatistics()
        content = {"Content":self.getContent()}
        return {**data,**content}
        
    def getContent(self):
        time.sleep(2)
        src=""
        try:
            src= self.driver.find_element(By.TAG_NAME, 'video').get_attribute("src")
        except:
            print("Failed to collect src from ",self.url)
        return src
        
    def __getUserId(self):
        user=""
        try:
            user = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[1]/div[1]/a[2]/h3").text
        except:
            pass
        try:
            user =self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]/div[2]/div/a[2]/span[1]').text
        except:
            pass
        try:
            user = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[2]/div/a[2]/span[1]").text
        except:
            pass
        return user

    def __getUser(self):
        user=""
        try:
            user = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div/a[2]/span[2]').text
            idx=user[::-1].index('??')
            user = user[:len(user)-(idx+1)]
        except:
            pass
        try:
            user = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[1]/div[1]/a[2]/h4").text
        except:
            pass
        try:
            user = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[2]/div/a[2]/span[2]").text
            user = user.split("??")[0]
        except:
            pass
        return user

    def __getDescription(self):
        result=""
        try:
            result = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[1]/div[2]/span").text
        except:
            pass
        try:
            result=self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]/div[1]/div[2]').text
        except:
            pass
        try:
            result = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/span").text
        except:
            pass
        return result
    def __getLikes(self):
        result = ""
        try:
            result = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[1]/div[3]/button[1]/strong").text
        except:
            pass
        try:
            result = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[2]/button[1]/strong").text
        except:
            pass
        try:
            result = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[3]/button[1]/strong").text
        except:
            pass
        return result
        
    def __getCommentCount(self):
        result = ""
        try:
            result = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[1]/div[3]/button[2]/strong").text
        except:
            pass
        try:
            result = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[2]/button[2]/strong").text
        except:
            pass
        try:
            result = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[3]/button[2]/strong").text
        except:
            pass
        return result
        
    def __getShares(self):
        result=""
        try:
            result=self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[2]/button[3]/strong").text
        except:
            pass
        try:
            result=self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[1]/div[3]/button[3]/strong").text
        except:
            pass
        try:
            result = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[3]/button[3]/strong").text
        except:
            pass
        return result

        
    def __getPublicationDate(self):
        date="2000-01-01"
        try:
            date = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]/div[2]/div/a[2]/span[2]/span[2]").text
        except:
            pass
        try:
            date = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[1]/div[1]/a[2]").text
            date = date.split("??")[1]
        except:
            pass
        try:
            date = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[2]/div/a[2]/span[2]/span[2]").text
        except:
            pass
        date=date.replace(' ','')
        return formatDate(date)

    #checa se h?? a mensagem de video removido
    def __videoExists(self):
        try:
            self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div/p[1]")
            return False
        except:
            return True

class ProfileStatisticsCollector(TikTokCollector):
    def __init__(self,driver):
        super().__init__(driver)
    
    def getStatistics(self):
        if not self.__channelExists():
            stats = {"Url":self.url,'User':"","UserId":"","ProfileBio":"","Followers":"","Following":"","LikeCount":"","CollectionDate":datetime.now().strftime("%Y-%m-%d"),"Status":0}
            return stats
        stats={}
        stats["Url"]=self.url
        stats["User"]=self.__getProfileName()
        stats["UserId"]=self.__getProfileId()
        stats["ProfileBio"]=self.__getProfileBio()
        stats["Followers"]=self.__getProfileFollowers()
        stats["Following"]=self.__getProfileFollowing()
        stats["LikeCount"]=self.__getProfileLikeCount()
        stats["CollectionDate"] = datetime.now().strftime("%Y-%m-%d")
        stats["Status"]=1
        return stats

    def __getProfileBio(self):
        return self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div[1]/h2[2]").text
    
    def __getProfileFollowers(self):
        return self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div[1]/h2[1]/div[2]/strong").text
    
    def __getProfileLikeCount(self):
        return self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div[1]/h2[1]/div[3]/strong").text
    
    def __getProfileFollowing(self):
        return self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div[1]/h2[1]/div[1]/strong").text
    
    def __getProfileId(self):
        return self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/h2").text
    
    def __getProfileName(self):
        return self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/h1").text

    #checa se o perfil existe
    def __channelExists(self):
        try:
            self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/main/div/p[1]")
            return False
        except:
            return True
            
class CommentCollector(TikTokCollector):
    def __init__(self,driver):
        super().__init__(driver)
        self.login()
        
    def __scroll(self):
        SCROLL_PAUSE_TIME = 0.5
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                return last_height != 881
                break
            last_height = new_height
    
    def __commentScroll(self):
        #click comment button
        self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[2]/button[2]").click()
        #get container of comments
        comment_container = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[3]/div[2]/div[3]")
        current_height = 200
        flag = False
        while True:
            self.driver.execute_script("arguments[0].scrollTop = arguments[1]", comment_container, current_height)
            current_scroll_top = self.driver.execute_script("return arguments[0].scrollTop", comment_container)
            if current_height != current_scroll_top:
                if flag:
                    break
                else:
                    time.sleep(2)
                    flag = True
            if flag and current_height == current_scroll_top:
                flag = False
            current_height += 200
            time.sleep(0.5)


    def __addLogin(self):
        self.setUrl("https://www.tiktok.com/login/phone-or-email/email")
        time.sleep(60.0)
        with open("cookies.pkl","wb") as f:
            pickle.dump(self.driver.get_cookies(), f)
        
    def __getLogin(self):
        self.setUrl("https://www.tiktok.com/login/phone-or-email/email")
        with open("cookies.pkl", "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
                
    def login(self):
        try:
            with open("cookies.pkl", "rb"):
                pass
            self.__getLogin()
        except:
            self.__addLogin()        


    def getStatistics(self):
        debug = []
    
        comments = []
        altComments = False
        if not self.__scroll():
            self.__commentScroll()
            altComments = True
        i = 1
        while True:
            try:
                element = []
                try:
                    if altComments: 
                        element = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[3]/div[2]/div[3]/div[" + str(i) + "]") 
                    else:
                        element = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]/div[3]/div[2]/div[" + str(i) + "]")
                except:
                    pass
                comment_element = element.find_element_by_xpath('div[1]')
                try:
                    reply_element = element.find_element_by_xpath('div[2]')
                except:
                    reply_element = None
                comment_element_text = comment_element.text
                aux = comment_element_text.split("\n")
                limit = 4 if altComments else 5
                while len(aux) > limit:
                    aux[1] += " \n " + aux.pop(2)
                debug = aux
                username = aux[0]
                comment = aux[1]
                when = aux[2].rstrip("Reply")
                date = formatDate(when)
                likes = int(aux[3])
                replies = 0
                if reply_element:
                    replies = int(reply_element.text.split("\n")[-1].split("(")[1].rstrip(")"))
                d = {"Url":self.url,'User':username,"Content":comment,"LikeCount":likes,"RepliesCount":replies,"PublicationDate":date,"CollectionDate":datetime.now().strftime("%Y-%m-%d")}
                comments.append(d)
                i += 1
            except Exception as e:
                break
        return comments
   
if __name__ == "__main__":
    opts = webdriver.ChromeOptions()
    opts.add_argument("--window-size=1024,768")
    driver =  webdriver.Chrome("./chromedriver.exe",options=opts)
    api = VideoStatisticsCollector(driver)
    api.setUrl("https://www.tiktok.com/@ptbrasil/video/6938889295319026949")
    print(api.getMetadata())
    #driver.close()
