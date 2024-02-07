from django.urls import path   #导入路径相关配置
from . import  views  #导入视图views

urlpatterns = [
    path('index/blog/<int:id>', views.show_blog),  #默认访问book业务的首页
    path('home',views.show_home),
    path('index/comment/<int:id>', views.comment),
    path('index/delcomment/<int:id>', views.delcomment),
    path('list',views.show_list),
    path('classes',views.show_classes),
    path('classes/1',views.show_classes_1),
    path('classes/2',views.show_classes_2),
    path('classes/3',views.show_classes_3),
    path('search',views.show_search),
    path('result',views.search,name="result")
]