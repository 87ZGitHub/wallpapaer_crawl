# -*- coding: UTF-8 -*- 
import os
import io
import pycurl
import urllib
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def crawler(browser, path):
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
        for info in soup.find_all('div', class_="rg_meta notranslate"):
            count += 1
            infotext = info.text
            print infotext
            firimgurl = infotext.split('"ou":"')
            secimgurl = firimgurl[1].split('","ow":')
            imgurl = secimgurl[0]
            file_name = "%s.jpg" % str(count)
            file_path = os.path.join(path, file_name)
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

def is_valid_jpg(jpg_file):   
    if jpg_file.split('.')[-1].lower() == 'jpg':  
        with open(jpg_file, 'rb') as f:  
            f.seek(-2, 2)  
            return f.read() == '\xff\xd9'   
    else:  
        return True
    

def main():

    links = [
        ("https://www.google.com/search?biw=1200&bih=640&tbs=isz%3Aex%2Ciszw%3A1080%2Ciszh%3A1920&tbm=isch&sa=1&ei=156fWsLmNeKN0wKShqOIDg&q=phone+wallpaper&oq=phone+wallpaper&gs_l=psy-ab.3..0i67k1j0j0i67k1l4j0l2j0i67k1l2.278248.278248.0.282350.1.1.0.0.0.0.260.260.2-1.1.0....0...1c.1.64.psy-ab..0.1.259....0.UDQGcFyF5Ec", "others"),
        ("https://www.google.com/search?biw=1200&bih=640&tbs=isz%3Aex%2Ciszw%3A1080%2Ciszh%3A1920&tbm=isch&sa=1&ei=z56fWqreHM_c0wLau4-gBg&q=animal+phone+wallpaper&oq=animal+phone+wallpaper&gs_l=psy-ab.3...4912.7278.0.7412.10.9.0.0.0.0.279.785.2-3.3.0....0...1c.1.64.psy-ab..7.3.784...0j0i13k1j0i67k1.0.4rqgChoJ71Q", "animals")
    ]
    for link in links:
        browser = webdriver.Chrome()
        browser.get(link[0])
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
        #创建文件夹及路径
        dirname = '/Users/haki/Documents/' + link[1]
        os.mkdir(dirname)
        filepath = dirname + "/"
        #爬取文件
        crawler(browser, dirname)
        browser.quit()
        print 'Crawl Comoleted and Start filter and order' + link[1]
        #filepath = "/Users/haki/Documents/" + link[1]
        count = 0
        tf = 0
        for x in os.listdir(filepath):
            try:
                print x
                if is_valid_jpg(filepath + x):
                    print "true"
                    tf += 1
                    print str(tf) + "true"
                else:
                    count += 1
                    print str(count) + "fale"
                    os.remove(filepath + x)
            except:
                print x + "get error"
                os.remove(filepath + x)
        print "begin rename"
        newcount = 0
        for y in os.listdir(filepath):
            newcount += 1
            newname = str(newcount) + "st.jpg"
            print newname
            os.rename(filepath + y, filepath + newname)
        twocount = 0
        for z in os.listdir(filepath):
            twocount += 1
            twoname = str(twocount) + ".jpg"
            print twoname
            os.rename(filepath + z, filepath +twoname)    



if __name__ == "__main__": 
   main()
