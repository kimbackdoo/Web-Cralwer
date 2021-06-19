import requests
import os
import re

## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
import django
django.setup()

# 모델 임포트는 django setup이 끝난 후
class WebCrawling:

    def web_crawling(shop):  # def web_crawling(url, path, storeName,index):
        get_id = shop.shop_id
        get_pw = shop.shop_password
        posturl = shop.url

        # 헤더 설정
        header = {
            'referer': 'http://www.gaudistyle.co.kr/Login',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }

        login = {
            'mem_type:': 'A',
            'mem_userid': get_id,
            'mem_userpwd': get_pw,
            'mem_savechk': 'true',
            'user_id': get_id,
            'user_pwd': get_pw,
            'save_id1': 'on',
            'user_id': '',
            'user_pwd': ''
        }

        total_list = []  # 내보낼 list
        p = re.compile('img_[0-9]+')
        error_log = ""
        # Session 생성, with 구문 안에서 유지
        with requests.Session() as s:
            try:
                site = s.post(posturl + '/Login', headers=header)
                site.raise_for_status()  # 404 200인지
                print('cooookie')
                print(site.cookies.get_dict())

                r = s.get(posturl + '/LoginOK', headers=header, data=login, cookies=site.cookies)
                if r.text.strip() != "true":
                    raise Exception('로그인에 실패했습니다.')

                # 찜 목록
                gd_no_list = []
                w = s.get(posturl + '/jSel').json()
                print(w)

                if not w:
                    raise IndexError

                for i in w:
                    gd_no_list.append(i['gd_no'])

                print(gd_no_list)
                # 제품 설명 gd_no_list.len 만큼 for문을 돌려
                for gd_no in gd_no_list:  # 2번 돌림
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
                        if p.match(i):  # 정규식
                            img_list.append(w[0].get(i))

                    # img_list중에 None값 제외
                    img_list = list(filter(None, img_list))
                    data['img_list_new'] = img_list

                    total_list.append(data)

                    # 찜하기 해제
                    print('찜하기 해제')
                    jjim_flag = {'gd_no': gd_no, 'gd_flag': '0'}
                    w = s.post(posturl + '/sLike', data=jjim_flag)

            except requests.exceptions.HTTPError as e:
                print("Http Error:", e)
                error_log = str(e)

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
                return total_list, error_log

if __name__ == '__main__':
    wc = WebCrawling
    posturl = 'http://www.gaudistyle.co.kr'
    shop_data_dict = wc.web_crawling(posturl)
    print(shop_data_dict)