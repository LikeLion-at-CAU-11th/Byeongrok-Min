from django.urls import path
from posts.views import *

urlpatterns = [
    path('post_detail/<int:id>/', post_detail,),
    path('post_all/', get_all_posts,),
    path('new_post/', create_post, name="create_post"),
    path('comment/<int:id>/', get_comment, name='get_comment'),
    path('new_comment/<int:id>/', create_comment, name="create_comment"),
    path('timezone_post/', get_posts_between, name="post time"),
]