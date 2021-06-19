from bs4 import BeautifulSoup as bs
import requests
import os
import sys
import json
import re
import uuid
import rsa
import lzstring
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
import django
django.setup()


class NaverCrawling:

    def encrypt(key_str, uid, upw):
        def naver_style_join(l):
            return ''.join([chr(len(s)) + s for s in l])

        sessionkey, keyname, e_str, n_str = key_str.split(',')
        e, n = int(e_str, 16), int(n_str, 16)

        message = naver_style_join([sessionkey, uid, upw]).encode()

        pubkey = rsa.PublicKey(e, n)
        encrypted = rsa.encrypt(message, pubkey)

        return keyname, encrypted.hex()


    def encrypt_account(uid, upw):
        key_str = requests.get('https://nid.naver.com/login/ext/keys.nhn').content.decode("utf-8")
        return NaverCrawling.encrypt(key_str, uid, upw)

    #하드코딩 되어있는 id & pw 
    def naver_session(nid, npw):
        encnm, encpw = NaverCrawling.encrypt_account(nid, npw)

        s = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504]
        )
        s.mount('https://', HTTPAdapter(max_retries=retries))
        request_headers = {
            'User-agent': 'Mozilla/5.0'
        }

        bvsd_uuid = uuid.uuid4()
        encData = '{"a":"%s-4","b":"1.3.4","d":[{"i":"id","b":{"a":["0,%s"]},"d":"%s","e":false,"f":false},{"i":"%s","e":true,"f":false}],"h":"1f","i":{"a":"Mozilla/5.0"}}' % (bvsd_uuid, nid, nid, npw)
        bvsd = '{"uuid":"%s","encData":"%s"}' % (bvsd_uuid, lzstring.LZString.compressToEncodedURIComponent(encData))

        resp = s.post('https://nid.naver.com/nidlogin.login', data={
            'svctype': '0',
            'enctp': '1',
            'encnm': encnm,
            'enc_url': 'http0X0.0000000000001P-10220.0000000.000000www.naver.com',
            'url': 'www.naver.com',
            'smart_level': '1',
            'encpw': encpw,
            'bvsd': bvsd
        }, headers=request_headers)

        print(resp)



        return s


    def naver_cafe(shop,url):

        try:
            data = {}
            
            
            s = NaverCrawling.naver_session(shop.shop_id, shop.shop_password) #id, password
            print(1)
            #url = "https://cafe.naver.com/moodnslow/1217"
            #cafe_id = '29179343' # cafe_id를 알아내야함

            #url에서 board_id & cafe_id 가져오기
            
            board_id = url.rsplit('/', 1)[1] #
            req = requests.get(url)
            
            # HTML 소스 가져오기
            html = req.text
            
            soup = bs(html,'html.parser')
            p = re.search("var cafeId = (\d+);",str(soup))

            if p:
                cafe_id = p.group(1)
            
            posturl = "https://apis.naver.com/cafe-web/cafe-articleapi/cafes/"+cafe_id+"/articles/"+board_id+"?fromList=true&useCafeId=true&buid=d30dbfa7-1d10-48b3-b899-361c756bc1f8"
            #url2 = "https://apis.naver.com/cafe-web/cafe-articleapi/cafes/29179343/articles/1217?fromList=true&useCafeId=true&buid=d30dbfa7-1d10-48b3-b899-361c756bc1f8"
            #https://apis.naver.com/cafe-web/cafe-articleapi/cafes/카페id/articles/게시판id?fromList=true&useCafeId=true&buid=d30dbfa7-1d10-48b3-b899-361c756bc1f8
            w = s.get(posturl).json()
            img_list = []
            data['title'] = w['article']['subject']
            data['url'] = url
            data['detail'] = re.sub('\[\[\[CONTENT-ELEMENT-\d*\]\]\]<br />','',w['article']['content'])
            for i in w['article']['contentElements']:

                img_list.append(i['json']['image']['url']+'?type='+i['json']['image']['type'])

            data['img_list_new'] = img_list
            
            print(data)

        except Exception as e:
            print('Exception 에러 발생!')
            print(str(e))
            error_log = str(e)
        else:
            error_log = "성공했습니다."
        finally:
            return data,error_log
            

    def naver_blog(url):
        
        header = {
            'referer' : 'http://www.naver.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }

        headers = {
            'Referer': url,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'             
        }
    
        data = {}
        
        try:
                    
            req = requests.get(url,headers= header)
            # HTML 소스 가져오기
            html = req.text
            header = req.headers
            status = req.status_code
            is_ok = req.ok

            soup = bs(html,'html.parser')

            
            # id가 mainFrame인 iframe src 가져오기

            #if mainFrame 있다면 (https://blog.naver.com/monica4460/221776101200)이런식이라면
            if soup.select_one('#mainFrame') is not None: #mainFrame 존재하는 url임
                mainFrame_src = soup.select_one('#mainFrame')['src']

                mainFrame_url = 'https://blog.naver.com' + mainFrame_src
                req = requests.get(mainFrame_url.strip(), headers= headers) #header추가하기 
                html = req.text   
                
            else:
                html = req.text
                
     
            soup = bs(html,'html.parser')

            
            #title = soup.select_one('div.se-title-text span').text
            print(soup.select_one('div.se-title-text span')) #None
            if soup.select_one('div.se-title-text span') is None:
                raise Exception("url 잘 못 함 ")
            else:
                title = soup.select_one('div.se-title-text span').text                

            #특수문자 제거(파 일 생성 안됨)
            title = re.sub('[\/:*?"<>|]','-',title).strip()
    
            data['title'] = title # 제품 명 

            category = soup.select_one('div.blog2_series a.pcol2').text
            print(category)
            data['category'] = category

            id_nickname = soup.select_one('a.link.pcol2').text
            print(id_nickname)
            data['storeName'] = id_nickname
            
            date = soup.select_one('span.se_publishDate.pcol2').text
            print(date)
            data['date'] = date
            data['url'] = url
            
            #contents
            #contents = soup.select('div.se-main-container span.se-fs-.se-ff-')
            contents = soup.select('div.se-main-container div.se-module span')
            print('contents')
            print(contents)

            
            
            text = ""

            for i in contents:
                #print(i.text)
                if i.text.strip(): #띄어쓰기 삭제 
                    print(i.text)
                    text += i.text+'<br>\n'


            
            #text = [text + i.text if not i for i in contents]
                
            
            print(text)
            data['detail'] = text
             

       
            imgs = soup.select('img.se-image-resource')
            img_list = []
           
            for i in imgs:

                #블러 처리 지우기
                match_object = re.search('(\?type=w(\d+)_blur)$',i['src'])
                if match_object:
                    a = match_object.group()#매치된 문자열
                    i['src']= i['src'].replace(a,"?type=w966")
            
                
                img_list.append(i['src'])
                
            data['img_list_new'] = img_list
            print(len(img_list))

        except requests.exceptions.HTTPError as e:
            print ("Http Error:",e)
            error_log = str(e)
                 
        except Exception as e:
            print('Exception 에러 발생!')
            print(str(e))
            error_log = str(e)
            
        else:
            error_log = "성공했습니다."
        finally:
            return data,error_log
            
            
            
        
if __name__=='__main__':
    sc = NaverCrawling
    posturl = 'https://blog.naver.com/monica4460/221859608124'
#    posturl = 'https://blog.naver.com/greenhouse4u/221985866146'
    sc.naver_blog(posturl)


    
        
