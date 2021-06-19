from django.shortcuts import render
from examples.models import Parsed_data, Shop
from django.db.models import Q
import json
from django.core.paginator import Paginator
# Create your views here.



def searchResult(request):
    products = None
    query = None
    final = []
    param = ""
    if 'q' in request.GET:
        param = 'q'
        query = request.GET.get('q')
        document_list = Parsed_data.objects.all().filter(Q(title__contains = query) | Q(f_k__title__contains = query)).order_by('-id')
        index= 0
        
        
    #거래처, 신상마켓, 네이버, 카카오스토리 
    elif 's' in request.GET:
        param = 's'
        query = request.GET.get('s') #거래처
        print(query)
        index= 0
             
        #Other check 안된 거래처 들의 data
        if query =="거래처": #거래처 클릭했다면 
            document_list = Parsed_data.objects.all().filter(Q(f_k__other_chk = False)).order_by('-id')
            #document_list = Parsed_data.objects.all().filter(Q(title__contains = query) | Q(f_k__title__contains = query)).order_by('-id')
            
        else: #거래처 아닌 거 
            document_list = Parsed_data.objects.all().filter(Q(f_k__other_chk = True) & Q(f_k__title__contains = query)).order_by('-id')

    else:
        
        document_list = [] #빈 값
        
        
    for i in document_list:

        a = []
        img_cnt = 0
        d = []

        if(i.img_data.first()):
            for j in i.img_data.all():
                d = json.loads(j.img_url_list)
                img_cnt = j.img_cnt #img 개수
                image_folder_path = j.img_folder_path
                
                #

        a.append(i)
        a.append(img_cnt)
        a.append(d)
        a.append(image_folder_path)
        
        index += 1
        final.append(a)
            

     
    paginator = Paginator(final,12)
    length = len(final)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    page_string = param+"="+query+"&"
    return render(request, 'search.html', {'page_string':page_string, 'query':query, 'posts':posts })






