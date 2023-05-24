from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Post, Comment
import json
# created_at 과제에서 시간 설정을 위한 모듈
from datetime import datetime

# 8주차 DRF serializer -->
from .serializers import PostSerializer, CommentSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
# <-- 8주차 


# Django에서 views.py의 역할: 웹클라이언트의 요청을 받고, DB에서 데이터를 받아 응답하는 역할. 
# 클라이언트가 post를 GET(READ), PATCH(UPDATE), DELETE(DELETE) 하고 싶다는 요청을 받는다.  
# 클라이언트의 요청에 따라 DB(posts/model.py)에 접근하여 Json 형식으로 가공해 Response를 보낸다. 

class PostList(APIView):
    def post(self, request, format=None):
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True) # 많은 값을 가져올 때는 다중값인 'many'를 True로 한다. 
        return Response(serializer.data)
    
# PostDetail : 하나씩 처리하는 클래스
class PostDetail(APIView):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    # put은 전체를 수정, fetch는 일부를 수정할 때 사용하는 Http 메서드
    def put(self, request, id):
        post = get_object_or_404(Post, id = id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        post = get_object_or_404(Post, id=id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CommentList(APIView):
    def post(self, request, id): # id 값을 가지는 게시물에 댓글 생성
        request.data["post"] = id
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id): # id 값을 가지는 게시물의 모든 댓글을 조회
        comments = Comment.objects.filter(post=id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
class CommentDetail(APIView):
    def get(self, request, id):
        comment = get_object_or_404(Comment, id=id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    def put(self, request, id):
        comment = get_object_or_404(Comment, id=id)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        comment = get_object_or_404(Comment, id=id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# week9

# mixins view
from rest_framework import mixins
from rest_framework import generics

# mixins는 generics 상속 받음
# create 담당: mixins.CreateModelMixin
# post는 id갑 부여해서 하는 게 아니라서 List 단에서 해주기
class PosListMixins(mixins.ListModelMixin,  mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
# get 담당 : mixins.RetrieveModelMixin, udpate 담당: mixins.UpdateModelMixin , delete 담당: mixins.DestroyModelMixin
class PostDetailMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
# genericsAPIView
class PostListGenericAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetailGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# viewset
from rest_framework import viewsets

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# post_list = PostViewSet.as_view({
#     'get': 'list',
#     'post': 'create',
# })

# post_detail_vs = PostViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })


