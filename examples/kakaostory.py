from selenium import webdriver
import chromedriver_binary
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import os
import sys
import json
import re
import pickle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

#카카오 api --> 이미지 최대 3 --> X 
#requests --> email & password 암호화 + 갱신   --> salt 모름 X 
#selenium 사용 --> O (개느림 사용자가 크롬 드라이버 업데이트 해야줘야함 .........ㅁㄴㅇㄹ)
#로그인만 api + 나머지 crawling 을 requests --> X
#

class KasCrawling:
    
    def get_driver():
        #headless로 변경하기
        
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

    
        driver = webdriver.Chrome(executable_path = r'./chromedriver_win32/chromedriver.exe',chrome_options=options) #executable_path = r'./chromedriver_win32/chromedriver.exe'
       
        driver.implicitly_wait(3)
        
        return driver
    

    def login_kakao(shop,driver):
    

        driver.get('https://accounts.kakao.com/login/kakaostory')

        user_id = shop.shop_id #shop.shop_id
        user_pw = shop.shop_password #shop.shop_password  
        
        #로그인 성공 
        driver.find_element_by_xpath('//*[@id="id_email_2"]').send_keys(user_id)
        driver.find_element_by_xpath('//*[@id="id_password_3"]').send_keys(user_pw)
        driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button').click() #로그인 확인
        #다음페이지 넘어감
        #print(driver.current_url) # https://accounts.kakao.com/login/kakaostory
        
        time.sleep(1)
        
        #print(driver.current_url)
        
        if (driver.current_url != "https://story.kakao.com/"):
            print("카카오스토리 로그인이 실패되었습니다.")
            return False
            
        else:
            print('카카오스토리 로그인이 되었습니다.')
                    
        
        return True
                
    
    def kas_crawling(shop,url):

        try: 
            driver = KasCrawling.get_driver()
            login = KasCrawling.login_kakao(shop,driver)

            data = {} # 보낼 데이터
            
            if login:
                print('로그인 됨')
                driver.get(url)
                soup = bs(driver.page_source, 'html.parser')
                
                script = str(soup.find_all('script')[1]).split('\n')

                #sripte 태그 + 불필요한 부분 제거 + 제이슨 형식으로 변경
                test = script[1].replace("boot.parseInitialData(",'')
                test = test.replace( ");" , '')

                #print(test)
                
                #test.raise_for_status()#404 200인지 # 'str' object has no attribute 'raise_for_status'
                

                #image 원본 url 저장할 배열
                img_urls = []
    
                #json 로드가 실패하면
                data2 = json.loads(test)
                #print(json.dumps(data, indent=4, sort_keys=True)) 
                #print(data2['activity'])

                
                getCreatedDate = data2['activity']['created_at'].split('T')
                data["date"] = str(getCreatedDate[0])

                #print(data)
                #제품 정보
                data['detail'] = data2['activity']['content']
                #이미지 정보
                images = data2['activity']['media']
                #아이디
                data['title'] = data2['activity']['actor']['display_name']

                #url
                data['url'] = url
                

                img_urls = [] 
                for img in images: 
                    img_urls.append(img['origin_url'])
                    
                data['img_list_new'] = img_urls
                #print(data)

                
            else :
                raise Exception('카카오스토리 로그인이 실패되었습니다.')


        except KeyError:
            error_log = str('url이 잘못되었습니다.')
            
        except Exception as e:
            print(str(e))
            error_log = str(e)

        else:
            error_log = "성공했습니다." 

        finally:
            
            driver.quit()
            return data, error_log
       
        
if __name__=='__main__':
    sc = KasCrawling
    posturl = 'https://story.kakao.com/blackoneday/iIq14DtUsSA'
    sc.kas_crawling(posturl)


    
        
