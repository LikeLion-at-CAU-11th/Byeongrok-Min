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

# mixins view
# urlpatterns = [
#     path('', PosListMixins.as_view()),
#     path('<int:pk>/', PostDetailMixins.as_view()),
#     path('<int:pk>/comment/', CommentListMixins.as_view()),
#     path('comment/<int:pk>/', CommentDetailMinxins.as_view())
# ]

# genericsAPIView
# <int:id>가 아닌 <int:pk>인 것을 생각.
# urlpatterns = [
#     path('', PostListGenericAPIView.as_view()),
#     path('<int:pk>/', PostDetailGenericAPIView.as_view()),
#     path('<int:pk>/comment/', CommetListGenericAPIView.as_view()),
#     path('comment/<int:pk>', CommentDetailGenericAPIView.as_view())
# ]

# viewSet
# urlpatterns = [
#     path('', post_list),
#     path('<int:pk>/', post_detail_vs),
#     path('<int:pk>/comment', comment_list),
#     path('comment/<int:pk>', comment_detail_vs)
# ]

# router = DefaultRouter()
# router.register('', PostViewSet)
# router.register('comment', CommentViewSet, basename='comment router')

# comment_router = DefaultRouter()

# urlpatterns = [
#     path('', include(router.urls)), 
# ]