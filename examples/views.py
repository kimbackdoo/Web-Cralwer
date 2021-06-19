from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, render, get_list_or_404, redirect

from bootstrap_modal_forms.generic import (BSModalLoginView,
                                           BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView
                                           )

from .forms import BookForm, CustomUserCreationForm, CustomAuthenticationForm, SetPathForm
from .models import Shop, Parsed_data, Img_data, Other
from .shop_crawler_request import WebCrawling
from .sinsang import SinsangCrawling
from .shop_crawler_multi import WebCrawling_T
from .naver import NaverCrawling
from .kakaostory import KasCrawling
import json as simplejson
import json
import os
import requests
import time
from multiprocessing import Pool
from django.core.paginator import Paginator
import html
import re
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse



#用
def Index(request):
    

    context = Shop.objects.exclude(other_chk=True)
    return render(request,'index.html',{'shops':context})

    

class BookCreateView(BSModalCreateView):
    template_name = 'examples/create_book.html'
    print(BookForm)
    form_class = BookForm
    success_message = 'Success: Shop was created.'
    success_url = reverse_lazy('index')


class BookUpdateView(BSModalUpdateView):
    model = Shop
    template_name = 'examples/update_book.html'
    form_class = BookForm
    success_message = 'Success: Shop was updated.'
    success_url = reverse_lazy('index')


class BookReadView(BSModalReadView):
    model = Shop
    template_name = 'examples/read_book.html'


class BookDeleteView(BSModalDeleteView):
    model = Shop
    template_name = 'examples/delete_book.html'
    success_message = 'Success: Shop was deleted.'
    success_url = reverse_lazy('index')


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'examples/signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('index')


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'examples/login.html'
    success_message = 'Success: You were successfully logged in.'
    success_url = reverse_lazy('index')


    
def Other(request):
    
    context = Shop.objects.exclude(other_chk=False)
    return render(request,'other.html',{'others':context})


#안씀 
class PathsetView(BSModalCreateView):#BSModalCreateView
    form_class = SetPathForm
    template_name = 'examples/set_path.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('index')

    
    model = Shop
    template_name = 'examples/set_path.html'
    form_class = SetPathForm
    success_message = 'Success: Shop was updated.'
    success_url = reverse_lazy('index')


    

def result(request, pk):
    
    # 时间 
    t0 = time.time()



    if request.method == 'POST':
        shop = get_object_or_404(Shop, pk=pk)

        
        
        #cetain_shop = Shop.objects.get(id=pk)#1개의 결과만 호출
        #print(cetain_shop.url)

        
        wc_data = WebCrawling.web_crawling(pk)

        data_list, error_log = wc_data
        
        
        print(error_log)


        img_list = []


            
        for shop_data_dict in data_list:



            
            
            #incoding
            #shop_data_dict['detail'] = shop_data_dict['detail']
            
            img_list = shop_data_dict['img_list_new']
                 
            
            del shop_data_dict['img_list_new'] #각각의 img_list_new삭제

            #내 로컬에 저장
            save_to_local(shop_data_dict, img_list)   
            
            #DB에 저장 
        
            P_d = Parsed_data(**shop_data_dict, f_k = shop)
            P_d.save()
            
            #print(P_d.id)

            
            Parsed_data_object= Parsed_data.objects.get(id=P_d.id)
            
            #위의 pk 가져와서 img_list 저장하기
            Img_data(title = Parsed_data_object.title+'_이미지',img_cnt = len(img_list),img_url_list = simplejson.dumps(img_list), f_k = Parsed_data_object).save() 


            
            
            
        

        d = time.time() - t0
        print("duration: %.2f s." % d)
        print(type(img_list))
        return render(request,'result.html',{'shop':data_list, 'img_list': img_list,'error_log': error_log})

#用
def save_to_media(profile_img,title): #保存一个代表照片(profile)
    print(profile_img)
    print(title)
    img_file_name = 'examples/static/img/'+title+'.jpg'
    
    r = requests.get(profile_img)
    file = open(img_file_name,"wb")
    file.write(r.content)
    file.close()
        
    return False


    
def save_to_local(shop_data_dict,img_list,path_directory,shop):

    try:

        if not path_directory:
            raise Exception('path가 빈값입니다.')

        #\을 /로 
        path_directory = path_directory.replace('\\','/')

        folder_name = shop_data_dict['title']
        folder_name = folder_name.replace(" ", "")
        folder = path_directory + '/' + shop + '-' + folder_name
        #folder = 'C:\Users\XNOTE\Downloads/' + folder_name
        img_list = img_list
    
        if not os.path.exists(folder): 
            os.makedirs(folder)            
            
    except OSError:
        print('Error : Creating folder with '+ folder )

    except Exception as e:
        print('Exception 에러 발생!')
        print(str(e))
        
    else:
        txt_file_location = folder + "/" + folder_name + ".txt"
        cleanr = re.compile('<.*?>')

        print(txt_file_location)
        #txt파일 저장 
        with open(txt_file_location, 'w', encoding='utf-8') as txtfile:
            for i in shop_data_dict.values():
                txtfile.write(html.unescape(re.sub(cleanr,'',str(i).replace('</p>','\n').replace('<br />','\n')))+"\n\n")
                
                            

        #이미지 저장
        key=0
        for img_file in img_list:
            img_file_name = folder + "/" + folder_name + '_' + str(key+1) + '.jpg'

            r = requests.get(img_file)
            file = open(img_file_name,"wb")
            file.write(r.content)
            file.close()
            
            key +=1

    

        return folder

def db(request):

    if request.is_ajax():
        dirName = request.POST.get('dirName', None)
        folder_open(dirName)

        
    #related_name을 활용한 역참조
    #document = Parsed_data.objects

    #document.img_data.all()

        
    #print(document)
    document_list = Parsed_data.objects.all().order_by('-id')  #내림차순
    
    index= 0
    final = []

    for i in document_list:

        a = []
        img_cnt = 0
        d = []

        if(i.img_data.first()):
            for j in i.img_data.all():
                d = json.loads(j.img_url_list)
                img_cnt = j.img_cnt #img 개수
                image_folder_path = j.img_folder_path
                

        a.append(i)
        a.append(img_cnt)
        a.append(d)
        a.append(image_folder_path)
        
        index += 1
        final.append(a)
        
     
    paginator = Paginator(final,12)#15
    length = len(final)
    page = request.GET.get('page')
    posts = paginator.get_page(page)



        
    
    return render(request,'db.html', {'posts':posts,'length':length})

def folder_open(dirName):
    path = dirName #C:\Users\metasoft\Downloads\네이버 블로그-트윌그물 5C
    path = os.path.realpath(path)
    os.startfile(path)


@require_POST # 해당 뷰는 POST method 만 받는다.
def ajax(request):
    
    pk = request.POST.get('pk', None) # ajax 통신을 통해서 template에서 POST방식으로 전달
    shop = get_object_or_404(Shop, pk=pk)

    path_directory = shop.path
    shop_title = shop.title

    wc_data = WebCrawling.web_crawling(shop)

    data_list, error_log = wc_data
    


    img_list = []

    for shop_data_dict in data_list:

        #shop_data_dict['detail'] = shop_data_dict['detail']

        
        img_list = shop_data_dict['img_list_new']
             
        
        del shop_data_dict['img_list_new'] #각각의 img_list_new삭제


        img_folder_path = save_to_local(shop_data_dict, img_list, path_directory, shop_title)   
        
    
        P_d = Parsed_data(**shop_data_dict, f_k = shop)
        P_d.save()
        
        #print(P_d.id)

        
        Parsed_data_object = get_object_or_404(Parsed_data, id=P_d.id)
        
        #위의 pk 가져와서 img_list 저장하기
        Img_data(title = Parsed_data_object.title+'_이미지',img_cnt = len(img_list),img_url_list = simplejson.dumps(img_list), img_folder_path = img_folder_path, f_k = Parsed_data_object).save() 



    context = {'error_log': error_log}

    return HttpResponse(json.dumps(context), content_type="application/json")
# context를 json 타입으로
    
    
@require_POST # 해당 뷰는 POST method 만 받는다.
def ajax_together(request):
    
    pk_list = request.POST.getlist('pk[]', None)
    pk_list = list(filter(None, pk_list))
    
    shop_object_list = list(Shop.objects.filter(pk__in=pk_list))
    

    wc_data_t = WebCrawling_T(pk_list,shop_object_list)#shop_object_list
    data_list = wc_data_t.web_crawling_together()


    error_list = []
    print(len(data_list),'개')

    index=0
    for i in data_list:
        
        error_list.append(i[1]+'\n')
        
        for j in i[0]:
            print(j['title'])#
        
            img_list = j['img_list_new']

            path_directory = shop_object_list[index].path 
            shop_title = shop_object_list[index].title  
            
            del j['img_list_new'] 

            #내 로컬에 저장
            img_folder_path = save_to_local(j, img_list, path_directory, shop_title)   
            #DB에 저장
            print('DB에 저장')
            print(shop_object_list[index])
            P_d = Parsed_data(**j, f_k = shop_object_list[index]) #f_k 순서 주
            P_d.save()

            Parsed_data_object = get_object_or_404(Parsed_data, id=P_d.id)
            #위의 pk 가져와서 img_list 저장하기
            Img_data(title = Parsed_data_object.title+'_이미지',img_cnt = len(img_list),img_url_list = simplejson.dumps(img_list), img_folder_path=img_folder_path, f_k = Parsed_data_object).save()             

        index+=1

                
    print(error_list)
    
    context = {'error_log': error_list}

    return HttpResponse(json.dumps(context), content_type="application/json")

# context를 json 타입으로
    
    
@require_POST # 해당 뷰는 POST method 만 받는다.
def setpath2(request):
    totalpath = request.POST.get('totalpath', None).strip()#
    print(totalpath)
    
    queryset = Shop.objects.all()
    queryset.update(path=totalpath) # 일괄 update 요청

    context = {'totalpath': totalpath}

    

    return HttpResponse(json.dumps(context), content_type="application/json")


#sinsang, naver, kakao crawl
@require_POST # 해당 뷰는 POST method 만 받는다.
def other_crawl(request):
    
    pk = request.POST.get('pk', None) # ajax 통신을 통해서 template에서 POST방식으로 전달
    crawl_url = request.POST.get('crawl_url', None).strip()

    if not crawl_url : #빈칸이면
        print('빈칸')
        
    name = request.POST.get('name', None).strip()
    
    shop = get_object_or_404(Shop, pk=pk)
    data = {}

    error_log =""
    
    #구별 
    if name == "신상마켓":
        wc_data = SinsangCrawling.singsang_crawling(shop,crawl_url)
        data, error_log = wc_data

    elif name == "네이버 블로그":
        print(crawl_url)
        wc_data = NaverCrawling.naver_blog(crawl_url)
        data, error_log = wc_data

    elif name =="카카오스토리":
        print(crawl_url)
        wc_data = KasCrawling.kas_crawling(shop,crawl_url)
        data, error_log = wc_data

    elif name =="네이버 카페":
        print(crawl_url)
        wc_data = NaverCrawling.naver_cafe(shop,crawl_url)
        data, error_log = wc_data
        
    
        
    else:
        wc_data = ""
            
    
    if data: #data 가 있다면
        
        img_list = data['img_list_new']     

        del data['img_list_new']
            
        path_directory = shop.path
            
        img_folder_path = save_to_local(data, img_list, path_directory, name)

        P_d = Parsed_data(**data, f_k = shop)
        P_d.save()
            
        Parsed_data_object = get_object_or_404(Parsed_data, id=P_d.id)
            
        Img_data(title = Parsed_data_object.title+'_이미지',img_cnt = len(img_list),img_url_list = simplejson.dumps(img_list), img_folder_path=img_folder_path, f_k = Parsed_data_object).save() 

        if name == "네이버 블로그":
            print('네이버 블로그')
            print(img_list[0])
            save_to_media(img_list[0],data['title']) 
    



            

    
    
    context = {'error_log': error_log }

    return HttpResponse(json.dumps(context), content_type="application/json")
