from django.db import models


class Other(models.Model):

    # There will be a default field with name "id" which is auto increment .
    title = models.CharField(max_length=50)
    url = models.URLField(default='')#url필드
    shop_id = models.CharField(default='',max_length=50, blank = True)#아이디 -> 암호화
    shop_password = models.CharField(default='',max_length=50, blank = True)#비밀번호
    path = models.CharField(max_length=200, blank = True) # 빈칸 가능 
    timestamp = models.DateField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title

    
class Shop(models.Model):

    # There will be a default field with name "id" which is auto increment .
    title = models.CharField(max_length=50)
    #publication_date2 = models.DateField(null=True)
    url = models.URLField(default='')#url필드
    shop_id = models.CharField(default='',max_length=50, blank = True)#아이디 -> 암호화
    shop_password = models.CharField(default='',max_length=50, blank = True)#비밀번호
    path = models.CharField(max_length=200, blank = True) # 빈칸 가능
    other_chk = models.BooleanField(default=False, blank=False)#Other탭인지 아닌지 
    #pages = models.IntegerField(blank=True, null=True)
    '''
    book_type = models.PositiveSmallIntegerField(choices=BOOK_TYPES)

    timestamp = models.DateField(auto_now_add=True, auto_now=False)
    '''


    def __str__(self): 
        return self.title  

class Parsed_data(models.Model):

    # There will be a default field with name "id" which is auto increment .
    f_k = models.ForeignKey(Shop, on_delete=models.CASCADE,default = '') #
    title = models.CharField(default='',max_length=50)
    notify = models.CharField(default='',max_length=50, blank = True, null=True)
    length = models.CharField(default='',max_length=50, blank = True, null=True)
    price = models.CharField(default='',max_length=50, blank = True, null=True)
    origin = models.CharField(default='',max_length=50, blank = True, null=True)
    style = models.CharField(default='',max_length=50, blank = True, null=True)
    model = models.CharField(default='',max_length=50, blank = True, null=True)
    model_botton = models.CharField(default='', max_length=50, blank=True, null=True)
    mxratio = models.CharField(default='',max_length=50, blank = True, null=True)
    date = models.CharField(default='',max_length=50, blank = True, null=True)   
    detail = models.TextField(default='', blank = True, null=True)    
    color = models.CharField(default='',max_length=50, blank = True, null=True)    
    size = models.CharField(default='',max_length=50, blank = True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True,  null=True)

    #추가
    storeName = models.CharField(default='',max_length=70, blank = True, null=True)
    tel = models.CharField(default='',max_length=50, blank = True, null=True)
    basicInfo = models.CharField(default='',max_length=50, blank = True, null=True)

    category = models.CharField(default='',max_length=50, blank = True, null=True)
    storeName = models.CharField(default='',max_length=50, blank = True, null=True)

    url = models.URLField(default='')#url필드

    def __str__(self):
        
        return self.f_k.title+'-'+self.title

    


class Img_data(models.Model):

    # There will be a default field with name "id" which is auto increment .
    f_k = models.ForeignKey(Parsed_data, on_delete=models.CASCADE,default = '', related_name='img_data') #
    title = models.CharField(default='',max_length=50, blank = True, null=True)
    img_cnt = models.IntegerField(blank=True, null=True)
    img_url_list = models.TextField(null=True) # JSON-serialized (text) version of your list
    #img_url = models.URLField(default='')#url필드
    img_folder_path = models.CharField(default='',max_length=50, blank = True, null=True) #이미지 로컬 폴더 위치 
    
    def __str__(self):
        return self.f_k.f_k.title+'-'+self.title



