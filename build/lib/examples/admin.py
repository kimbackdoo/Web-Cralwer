from django.contrib import admin

# Register your models here.

#models에서 BlogData를 import 해옵니다.
from .models import Book

admin.site.register(Book)
