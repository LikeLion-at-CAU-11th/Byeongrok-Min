from django.urls import path, include
from posts.views import *
# router 
# from rest_framework.routers import DefaultRouter

urlpatterns = [
    # 8주차 DRF
    # 보통 리스트는 url 안 써주는 것이 좋다. 
    path('', PostList.as_view()),
    path('<int:id>/', PostDetail.as_view()),
    path('<int:id>/comment/', CommentList.as_view()), # 해당 게시물(post)의 comment 처리. id == post_id
    path('comment/<int:id>', CommentDetail.as_view()) # 해당 comment 처리. id == comment_id
]