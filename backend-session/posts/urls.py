from django.urls import path
from posts.views import *

urlpatterns = [
    path('', hello_world, name = 'hello_world'),
    path('introduction/', introduction, name = 'introduction'), #name 은 필수는 아님. 유지보수에 쓰인다. 
    path('post_detail/<int:id>/', get_post_detail,),
    path('post_all/', get_all_posts,),
]