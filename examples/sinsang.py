from bs4 import BeautifulSoup as bs
import requests
import os
import sys
import json
import re
import hashlib
## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
import django
django.setup()

class SinsangCrawling:

    
    def singsang_crawling(shop,url):
        
        #url = "https://www.sinsangmarket.kr/v3/goodsDetail?gid=41692903"

        get_id = shop.shop_id
        get_pw = shop.shop_password
        
        #신상마켓 form data 비번-->암호화 64글자 -->sha256 해시함수 씀
        get_pw_hash = hashlib.sha256(get_pw.encode('utf-8')).hexdigest() # 해시 코드로 바꿈 

        
        # 로그인할 유저정보를 넣어줍시다. (모두 문자열입니다!)
        headers = {
            'referer': 'https://story.kakao.com/a/settings/profile?_=15910844264133',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }
        login = {
            'userid': get_id,
            'passwd': get_pw_hash, #
            'autologin': 'y',
            'is_ajax': '1'
        }
      
        data = {} # 보낼 데이터
        
        # Session 생성, with 구문 안에서 유지
        with requests.Session() as s:
            
            try:
                
                login_req = s.post('https://www.sinsangmarket.kr/api/requestLogin.php',headers=headers,data=login)

                login_req.raise_for_status()#404 200인지
                
                print(login_req.status_code)# 실패해도 200
                print(login_req.json())
                login_chk = login_req.json()
                oauth_token= ""
                print(login_chk['result'])
                if login_chk['result'] == "success":#and not(login_chk['result_mst'])
                    oauth_token = login_chk['oauth_token']
                    print('신상마켓 로그인에 성공')
        

                else:
                    raise Exception('신상마켓 로그인에 실패했습니다.') 
                    
                    



     
                # -- 여기서부터는 로그인이 된 세션이 유지 --

                
                #info_url ='https://www.sinsangmarket.kr/api/getSomeGoodsData?userid=syyang&gid=41692903&se=&oauth_token='            
                match_object =  re.search("\?gid=(\d+)",url)
                if match_object:
                    gid = match_object.group(1)
                else:
                    gid = ""
                    raise Exception('신상마켓 url을 다시 입력해주세요.')
                
                print(gid)#41692903 #NonType Error 발생 
                

                #여기서 raise 해주기

                #if gid 

                info_url = 'https://www.sinsangmarket.kr/api/getSomeGoodsData?userid='+get_id+'&gid='+gid+'&se=&oauth_token='
                info_url += oauth_token


                w = s.post(info_url,headers=headers).json()['gdata']
                
                data['title'] = w['goodsName']#제품 명 
                data['storeName'] = w['storeName'] #
                data['tel'] = w['tel'] # 전화번호
                #data['price'] = w['price'] # 23,000원
                data['price'] = w['goodsPrice'] # 23000
                data['color'] = w['color'] # 색상 
                data['size'] = w['size'] # 사이즈 
                data['mxratio'] = w['mixtureRate'] # 혼용률
                data['origin'] = w['madeInCountry'] #원산
                data['basicInfo'] = w['basicInfo']
                data['detail'] = w['intro'] # 제품 상세설명
                data['style'] = w['detailCategoryName'] # 스타일
                data['url'] = url

                #이미지 
                img_list = []
                for i in w['goodsImages']:
                    img_list.append('https://image-cache.sinsang.market?f='+i['imageUrl'] + i['filename']+'&h=907&w=690')

    #            print(img_list)
                data['img_list_new'] = img_list

                print(data)
                        

            
            except requests.exceptions.HTTPError as e:
                print ("Http Error:",e)
                error_log = str(e)

            #要再一次
            except IndexError:
                print('찜하기를 아직 누르지 않으셨습니다. 다시 눌러주세요')
                error_log = '찜하기를 아직 누르지 않으셨습니다. 다시 눌러주세요'
            
            except Exception as e:
                
                print('Exception 에러 발생!')
                print(str(e))
                error_log = str(e)
                
            else:
                error_log = "성공했습니다."

            finally:
                
                return data,error_log





           
                


        
if __name__=='__main__':
    sc = SinsangCrwaling
    posturl = 'https://www.sinsangmarket.kr//v3/goodsDetail?gid=3897071'
    sc.singsang_crawling(posturl)


    
        

