from django.urls import path

from . import views


urlpatterns = [
    #path('', views.Index.as_view(), name='index'),
    path('', views.Index, name='index'),    
    path('create/', views.BookCreateView.as_view(), name='create_book'),
    path('update/<int:pk>', views.BookUpdateView.as_view(), name='update_book'),
    path('read/<int:pk>', views.BookReadView.as_view(), name='read_book'),
    path('delete/<int:pk>', views.BookDeleteView.as_view(), name='delete_book'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    #path('post/', views.Index.as_view(), name='post_detail'),
    path('result/<int:pk>',views.result,name="result"),
    path('other/',views.Other, name="other"),
    #path('other/', views.Other.as_view(), name='other'),
    path('db/',views.db, name="db"),
    path('ajax/', views.ajax, name='ajax'),
    path('ajax_together/',views.ajax_together, name = 'ajax_together'),
    path('setpath2/',views.setpath2, name = 'setpath2'),
    path('other_crawl/',views.other_crawl, name = 'other_crawl'),
]

