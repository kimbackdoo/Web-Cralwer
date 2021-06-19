#+추가) 크롤링한 데이터 저장하기
import os
import re

## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
import django
django.setup()

from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import requests
import time

class WebCrawling_T:
    
    def __init__(self, pk_list, shop_object_list):#shop_object_list
        
        self.urls = []
        self.ids = []
        self.passwords = []

        print('list를 딕셔너리로 만들어주기')# {0:[url,id,pass],1:[],2:[]}

        key = 0
        self.new_dict = {}
        
        for i in shop_object_list:
            lst =  list(range(4))
            lst[0] = i.url
            lst[1] = i.shop_id
            lst[2] = i.shop_password
            lst[3] = i.title
            self.new_dict[key] = lst
            key+=1

        print(self.new_dict)


        #url찾기
        #self.urls = list(Shop.objects.filter(pk__in=pk_list).values_list('url', flat=True).distinct())
        #self.urls = ['http://www.gaudistyle.co.kr','http://www.dks08.co.kr','http://www.thedoorim.com']

        #헤더 설정
        self.header = {
            'referer' : 'http://www.gaudistyle.co.kr/Login',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
    
        
    
    def web_crawling_together(self):
        
        start_time = time.time()
        

        ##list를 딕셔너리로 만들어주기
        urls= self.new_dict
        #urls = {0:['url','id','pass'],1:['url','id','pass'],2:['url','id','pass']} #dict
        
        with Pool(processes=4) as pool:  
            result = pool.map(self.do_process_with_thread_crawl, urls.values())
            print("--- elapsed time %s seconds ---" % (time.time() - start_time))

        return result
        

    #def do_process_with_thread_crawl(self, url: str):
    def do_process_with_thread_crawl(self, url: list):


        result = self.do_thread_crawl(url)
        
        return result

        
    #def do_thread_crawl(self, url: str):
    def do_thread_crawl(self, url: list):
        thread_list = []


        with ThreadPoolExecutor(max_workers=8) as executor:
            thread_list.append(executor.submit(self.do_html_crawl, url))

            for execution in concurrent.futures.as_completed(thread_list):
                result = execution.result()

        return result

    
    #def do_html_crawl(self, posturl: str):#각각 crawling {'url','pw','id'}
    def do_html_crawl(self, posturls: list): #['url','pw','id']

        posturl = posturls[0]
        get_id = posturls[1]
        get_pw = posturls[2]
        title_ = posturls[3]

        total_list = []#내보낼 list
        p = re.compile('img_[0-9]+')

        # Session 생성, with 구문 안에서 유지
        with requests.Session() as s:
            try:
                login = {
                    'mem_type:' : 'A',
                    'mem_userid': get_id,
                    'mem_userpwd': get_pw,
                    'mem_savechk':'true',
                    'user_id': get_id,
                    'user_pwd': get_pw,
                    'save_id1':'on',
                    'user_id':'',
                    'user_pwd':''
                }

                site = s.post(posturl+'/Login', headers=self.header)
                site.raise_for_status()#404 200인지

                error_log = ""
                
                r = s.get(posturl + '/LoginOK', headers=self.header,data= login ,cookies = site.cookies)
                if r.text.strip() !="true":
                    raise Exception('로그인에 실패했습니다.')

                #찜 목록 
                gd_no_list = []
                w = s.get(posturl+'/jSel').json()

                if not w:
                    raise IndexError
                
                for i in w:
                    gd_no_list.append(i['gd_no'])
                print(gd_no_list)

                #제품 설명 gd_no_list.len 만큼 for문을 돌려
                for gd_no in gd_no_list:#2번 돌림
                    data = {}
                    jginfo = {}
                    img_list = []

                    jginfo['gd_no'] = gd_no
                    w = s.post(posturl + '/jGinfo', data=jginfo).json()
                    # json 형식으로 가져옴
                    print(w)

                    # 특수문자 제거(파일 생성 안됨) 후 제품명 가져오기
                    title = re.sub('[\/:*?"<>|]', '-', w[0]['gd_name1'])
                    data['title'] = title
                    print('[제품명: ' + title + ']')

                    # 상세 사이즈
                    length = "상세 사이즈 : " + w[0]['gd_sizestr']
                    data['length'] = length

                    # 가격
                    price = "가격 : " + str(w[0]['gd_vprice'])
                    data['price'] = price

                    # 원산지
                    origin = "원산지 : " + w[0]['gd_origin']
                    data['origin'] = origin

                    # 스타일
                    style = "스타일 : " + w[0]['gd_class1']
                    data['style'] = style

                    # 모델 정보
                    if w[0]['gd_modelstr'] == "":  # 쇼핑몰 사이트 마다 모델 정보가 다름 따라서 예외 처리
                        model = "모델정보 : " + w[0]['gd_info5']
                    else:
                        model = "모델정보 : " + w[0]['gd_modelstr'].split("||")[1]  # 모델 번호 빼기 (157||)이런거

                    data['model'] = model

                    # 혼용
                    mxratio = "혼용율 : " + w[0]['gd_matter3']
                    data['mxratio'] = mxratio

                    # 등록 일자
                    date = "등록일자 : " + w[0]['r_date']
                    data['date'] = date

                    # 세부정보
                    detail = "상세정보\n" + w[0]['gd_myinfostr']
                    data['detail'] = detail

                    # 색상선택
                    color = "-- 색상 --\n" + w[0]['gd_optcolornm'].replace("|", "\n")
                    data['color'] = color

                    # 사이즈
                    size = "-- 사이즈 --\n" + w[0]['gd_optsize']
                    data['size'] = size.split('|')[0]

                    # txt 파일 하단 모델정보
                    if w[0]['gd_modelstr'] == "":  # 쇼핑몰 사이트 마다 모델 정보가 다름 따라서 예외 처리
                        model_botton = "-- 모델정보 --\n" + w[0]['gd_info5']
                    else:
                        model_botton = "-- 모델정보 --\n" + w[0]['gd_modelstr'].split("||")[1]  # 모델 번호 빼기 (157||)이런거

                    data['model_botton'] = model_botton
                    
                    # 이미지
                    for i in w[0].keys():
                        if p.match(i): # 정규식 
                            img_list.append(w[0].get(i))

                    img_list = list(filter(None, img_list))
                    data['img_list_new'] = img_list
                     
                    total_list.append(data)


                    #찜하기 해제
                    print('찜하기 해제')
                    jjim_flag = {'gd_no':gd_no, 'gd_flag':'0'}
                    w = s.post(posturl+'/sLike',data=jjim_flag)
            
            except requests.exceptions.HTTPError as e:
                print ("Http Error:",e)
                error_log = '[{}] '.format(title_)+ str(e)
                
            except IndexError:
                print('[{}] 찜하기를 아직 누르지 않으셨습니다. 다시 눌러주세요'.format(title_))
                error_log = '[{}] 찜하기를 아직 누르지 않으셨습니다. 다시 눌러주세요'.format(title_)

            except Exception as e:
                print('Exception 에러 발생!')
                #print(str(e))
                print("[{}] ".format(title_) +str(e))
                error_log = '[{}] '.format(title_) + str(e)

            else:
                error_log = "[{}] 성공했습니다.".format(title_)              

            finally:
                return total_list, error_log
                    
if __name__=='__main__':
    start_time = time.time()
    urls = ['http://www.gaudistyle.co.kr','http://www.dks08.co.kr','http://www.thedoorim.com']
    #urls = ['http://www.gaudistyle.co.kr']

    # 멀티 쓰레드만 이용
    #for url in urls:
    #    print(WebCrawling.do_thread_crawl(url))
        
    #print("--- elapsed time %s seconds ---" % (time.time() - start_time))
    
    # 멀티 쓰레드 + 멀티 프로세스 
    with Pool(processes=4) as pool:  
        result = pool.map(WebCrawling_T.do_process_with_thread_crawl, urls)
        print("--- elapsed time %s seconds ---" % (time.time() - start_time))
    print(result)







