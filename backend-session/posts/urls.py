from django.urls import path
from posts.views import *

urlpatterns = [
    # 8주차 DRF
    # 보통 리스트는 url 안 써주는 것이 좋다. 
    path('', PostList.as_view()),
    path('<int:id>/', PostDetail.as_view()),
    path('comment/<int:id>/', CommentClass.as_view()),
]