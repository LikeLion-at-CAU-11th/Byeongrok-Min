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

# JWT 인가 구현
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from config.permissions import IsWriterOrReadOnly


# Django에서 views.py의 역할: 웹클라이언트의 요청을 받고, DB에서 데이터를 받아 응답하는 역할. 
# 클라이언트가 post를 GET(READ), PATCH(UPDATE), DELETE(DELETE) 하고 싶다는 요청을 받는다.  
# 클라이언트의 요청에 따라 DB(posts/model.py)에 접근하여 Json 형식으로 가공해 Response를 보낸다. 

# CBV, 클래스 뷰에는 APIView, Mixins, Generic CBV, ViewSet 4개의 종류가 있음.

# apiView: 함수 기반의 뷰로, 간단한 뷰 표현에 사용

# APIView 클래스를 상속 받아서 사용함 
# HTTP 메서드를 처리하는 로직이 구현되어 있음 / 파이썬의 상속 형식 -> class 자식클래스(부모클래스): ...

class PostList(APIView):
    # 로그인 한 사용자 -> 게시물 작성 읽기 가능
    # 로그인 안 한 사용자 -> 게시물 읽기만 가능
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # permission_classes = [IsAuthenticated] # 로그인 안 하면 모든 권한 없음
    
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True) # 많은 값을 가져올 때는 다중값인 'many'를 True로 한다. 
        return Response(serializer.data)
    
    def post(self, request, format=None):
        request.data['writer'] = request.user.id    # 현재 로그인된 user
        serializer = PostSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
    
# PostDetail : 하나씩 처리하는 클래스
class PostDetail(APIView):
    # 객체 수준에서 permission을 검사하는 함수가 별도로 필요
    def get_object(self, id):
        post = Post.objects.get(id=id)
        self.check_object_permissions(self.request, post)
        return post
    
    def get(self, request, id):
        post = Post.objects.get(id=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    # put은 전체를 수정, fetch는 일부를 수정할 때 사용하는 Http 메서드
    def put(self, request, id):
        post = Post.objects.get(id=id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        post = Post.objects.get(id=id)
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