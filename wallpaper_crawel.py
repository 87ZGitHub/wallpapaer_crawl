import os
import pycurl
import urllib
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def crawler(browser):
    #delay = 5
    print "start crwal"

    try:
        try:
            WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "rg_ilmbg")))
        except Exception as e:
            print e
        
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        print str(len(soup.find_all('div', class_='rg_meta notranslate')))
        count = 0
        # for info in soup.find_all('div', class_='rg_meta notranslate'):
        #     count += 1
        #     infotext = info.text
        #     print infotext
        #     firimgurl = infotext.split('"ou":"')
        #     secimgurl = firimgurl[1].split('","ow":')
        #     imgurl = secimgurl[0]
        #     file_name = "%s.jpg" % str(count)
        #     file_path = os.path.join("/Users/haki/Documents/nature", file_name)
        #     #urllib.urlretrieve(imgurl,file_path)
        #     pycurl_downlaod(imgurl, file_path, proxy_server=None)
        #     print "download:" + str(count)
        #     time.sleep(0.5)  


        for info in soup.find_all('div', class_="rg_meta notranslate"):
            count += 1
            infotext = info.text
            print infotext
            firimgurl = infotext.split('"ou":"')
            secimgurl = firimgurl[1].split('","ow":')
            imgurl = secimgurl[0]
            file_name = "%s.jpg" % str(count)
            file_path = os.path.join("/Users/haki/Documents/nature", file_name)
            #urllib.urlretrieve(imgurl,file_path)
            pycurl_downlaod(imgurl, file_path, proxy_server=None)
            print "download:" + str(count)
    except TimeoutException:
        print "Loading took too much time!"


def pycurl_downlaod(source_url, save_file, proxy_server=None):
    if len(save_file.split("/")) != 1:
        if not os.path.exists(os.path.dirname(save_file)):
            os.makedirs(os.path.dirname(save_file))
    try:
        file = open(save_file, 'w')
        curl = pycurl.Curl()
        try:
            print "1"
            curl.setopt(pycurl.URL, str(source_url))
            curl.setopt(pycurl.FOLLOWLOCATION, 1)
            curl.setopt(pycurl.WRITEDATA, file)
            curl.setopt(pycurl.CONNECTTIMEOUT, 60)
            curl.setopt(pycurl.TIMEOUT, 10000)
            curl.setopt(pycurl.USERAGENT, "cdn-unionread")
            if proxy_server:
                curl.setopt(pycurl.PROXY, str(proxy_server))
                curl.setopt(pycurl.PROXYPORT, 80)
                curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_HTTP)
            curl.setopt(pycurl.MAX_RECV_SPEED_LARGE, 20000000)  # 2M
            curl.perform()
            http_code = curl.getinfo(curl.HTTP_CODE)
            return dict(code=http_code, message='success')
        except:
            pass
        finally:
            curl.close()
            file.close()
    except Exception as e:
        print e
        try:
            os.remove(save_file)
        except:
            pass
        code = e.code if hasattr(e, 'code') else 0
        reason = str(e.reason) if hasattr(e, 'reason') else str(e)
        return dict(code=code, message=reason)

    

def main():

    link = 'https://www.google.com/search?biw=1099&bih=1343&tbs=isz%3Aex%2Ciszw%3A1080%2Ciszh%3A1920&tbm=isch&sa=1&ei=_5GeWp_mE8KQ0gKmvouoAg&q=natural+scenery&oq=natural+scenery&gs_l=psy-ab.12...0.0.0.43584010.0.0.0.0.0.0.0.0..0.0....0...1c..64.psy-ab..0.0.0....0.QH-TXhcN3M8'

    browser = webdriver.Chrome()
    browser.get(link)
    # browser.refresh()
    i = 0
    for i in [0,1,2,3]:
        print str(i)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        i += 1
    browser.find_element_by_id("smb").click()
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    # elem.send_keys(Keys.ENTER)


    #browser.execute_script("document.documentElement.scrollTop=4000")
    crawler(browser)

    #browser.quit()
    print 'Comoleted'

if __name__ == "__main__": 
   main()
