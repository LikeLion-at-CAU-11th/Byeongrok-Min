from django.urls import path
from posts.views import *

urlpatterns = [
    # [FBV일 때 urls.py 형식 | path('사용자url', 함수명, 별칭)]
    
    # path('post_detail/<int:id>/', post_detail,),
    # path('post_all/', get_all_posts,),
    # path('new_post/', create_post, name="create_post"),
    # path('comment/<int:id>/', get_comment, name='get_comment'),
    # path('new_comment/<int:id>/', create_comment, name="create_comment"),
    # path('timezone_post/', get_posts_between, name="post time"),

    # 8주차 DRF
    # 보통 리스트는 url 안 써주는 것이 좋다. 
    path('', PostList.as_view()),
    path('<int:id>/', PostDetail.as_view())

    
]