from django.db import models


class Book(models.Model):
    HARDCOVER = 1
    PAPERBACK = 2
    EBOOK = 3
    BOOK_TYPES = (
        (HARDCOVER, 'Hardcover'),
        (PAPERBACK, 'Paperback'),
        (EBOOK, 'E-book'),
    )
    title = models.CharField(max_length=50)

    publication_date = models.DateField(null=True)
    author = models.CharField(max_length=30, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pages = models.IntegerField(blank=True, null=True)
    book_type = models.PositiveSmallIntegerField(choices=BOOK_TYPES)

    timestamp = models.DateField(auto_now_add=True, auto_now=False)


'''
from django.db import models


class Book(models.Model):
    HARDCOVER = 1
    PAPERBACK = 2
    EBOOK = 3
    BOOK_TYPES = (
        (HARDCOVER, 'Hardcover'),
        (PAPERBACK, 'Paperback'),
        (EBOOK, 'E-book'),
    )
    title = models.CharField(max_length=50)
    url = models.URLField()#url필드
    path = models.CharField(max_length=200, blank = True) # 빈칸 가능 
    #publication_date = models.DateField(null=True)
    #author = models.CharField(max_length=30, blank=True)
    #price = models.DecimalField(max_digits=5, decimal_places=2)
    #pages = models.IntegerField(blank=True, null=True)
    #book_type = models.PositiveSmallIntegerField(choices=BOOK_TYPES)

    #timestamp = models.DateField(auto_now_add=True, auto_now=False)

    shop_id = models.CharField(default='',max_length=200, blank = True)#아이디 -> 암호화
    password = models.CharField(default='',max_length=200, blank = True)#비밀번호

'''
