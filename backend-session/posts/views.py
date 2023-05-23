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


# @require_http_methods(["GET", "PATCH", "DELETE"])
# def post_detail(request, id):
#     if request.method == "GET":

#         post = get_object_or_404(Post, pk = id) #id를 pk로 사용한다. post변수에 해당 id의 wirter, content, category 정보를 넘겨준다. 
        
#         category_json={
#             "id": post.id, #primary key
#             "writer": post.writer,
#             "content": post.content,
#             "category": post.category,
#         }

#         return JsonResponse({
#             'status': 200,
#             'message': '게시글 조회 성공',
#             'data':category_json
#         })
#     # 클라이언트 요청을 if-elif로 분기 처리. 
#     # PATCH : Update 기능이지만 일부만 업데이트 한다는 점이 PUT과 차이가 있음.
#     elif request.method == "PATCH":
#         body = json.loads(request.body.decode('utf-8')) # body에 문자를 utf-8로 디코딩.
#         update_post = get_object_or_404(Post, pk=id)

#         update_post.content = body['content']
#         update_post.category = body['category']
#         update_post.save() # orm 저장
#         # 여기서 끝내도 되지만, 수정 사항을 보여주기 위해 작성함. 
#         update_post_json = {
#             "id":update_post.id,
#             "writer":update_post.writer,
#             "content":update_post.content,
#             "category":update_post.category,
#         }

#         return JsonResponse({
#             'status': 200,
#             'message': '게시물 수정 성공',
#             'data': update_post_json,
#         })
#     elif request.method == "DELETE":
#         delete_post = get_object_or_404(Post, pk=id)
#         delete_post.delete()

#         return JsonResponse({
#             "status": 200,
#             "message": "게시물 삭제 성공"
#         })

# @require_http_methods(["GET"]) #데코레이터. 아래 함수를 감싸는 함수로서 여기서는 GET 이외의 요청이 왔을 떄 오류 메시지를 전달한다. 
# def get_all_posts(request):
#     all_post = Post.objects.all()
#     post_list = [] # 공백 리스트를 만들고 append를 통해 id 순서대로 넣어준다. 
#     for x in all_post:
#         post_info={
#         "id": x.id,
#         "writer": x.writer,
#         "content": x.content,
#         "category": x.category,
#         }
#         post_list.append(post_info)

#     return JsonResponse({
#         'status': 200,
#         'message': '모든 post 게시글 조회 성공',
#         'data': post_list # post_info를 담고 있는 post_list를 출력한다. 
#     })

# # CREATE
# @require_http_methods(["POST"])
# def create_post(request):
#     body = json.loads(request.body.decode('utf-8'))

#     new_post = Post.objects.create(
#         writer = body['writer'],
#         content = body['content'],
#         category = body['category'],
#     )

#     new_post_json = {
#         "id":new_post.id,
#         "writer":new_post.writer,
#         "content":new_post.content,
#         "category":new_post.category,
#     }

#     return JsonResponse({
#         'status': 200,
#         'message': '게시물 목록 조회 성공',
#         'data': new_post_json,
#     })

# # READ
# @require_http_methods(["GET"])
# def get_comment(request, id):
#     # Django ORM의 filter() 메서드 : 모델 필드를 비교하고, 조건을 충족하는 객체를 반환. 
#     # 필드? Django 모델에서는 DB 테이블의 열(column)에 해당. 각 필드는 모델 클래스 내에서 클래스 변수로 선언. 
#     comment_all = Comment.objects.filter(post = id)
#     comment_json_list = []
#     for comment in comment_all:
#         comment_json = {
#             'writer':comment.writer,
#             'content':comment.content,
#         }
#         comment_json_list.append(comment_json)

#     return JsonResponse({
#         'status': 200,
#         'message': "댓글 읽어오기 성공",
#         'data': comment_json_list
#     })

# # create comment
# @require_http_methods(["POST"])
# def create_comment(request, id):
#     body = json.loads(request.body.decode('utf-8'))

#     # commet를 입력할 post 지정. 
#     target_post = Post.objects.get(id = id)

#     writer = body['writer']
#     content = body['content']
    
#     # Comment model의 post를 target_post와 연결. 
#     new_comment = Comment.objects.create(
#         writer=writer,
#         content=content,
#         post = target_post,
#     )

#     new_comment_json = {
#         "writer":new_comment.writer,
#         "content":new_comment.content,
#     }

#     return JsonResponse({
#         'status':200,
#         'message': '댓글 추가 성공',
#         'data': new_comment_json,
#     })

# # GET posts that created between two sessions

# @require_http_methods(["GET"])
# def get_posts_between(request):
#     # 지난 세션 이후 시간
#     session1_time = datetime(2023, 4, 5, 22, 1)
#     # 다음 세션 이전 시간
#     session2_time = datetime(2023, 4, 12, 18, 58)

#    # time_post = Post.objects.filter(created_at__range=(session1_time, session2_time))
#     time_between_post = Post.objects.filter(created_at__range=[session1_time, session2_time])

#     post_list = [] # 공백 리스트를 만들고 append를 통해 id 순서대로 넣어준다. 
#     for x in time_between_post:
#         post_info={
#         "id": x.id,
#         "writer": x.writer,
#         "content": x.content,
#         "category": x.category,
#         "created_time": x.created_at,
#         }
#         post_list.append(post_info)

#     return JsonResponse({
#         'status': 200,
#         'message': '두 세션 사이에 생성된 게시글 조회 성공',
#         'data': post_list # post_info를 담고 있는 post_list를 출력한다. 
#     })

# 8주차 [ModelSerializer]
# PostList : 한번에 가져오거나 처리하는 클래스
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
    

class CommentClass(APIView):
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
    
    def delete(self, request, id): # 여기서 id 값은 comment의 id 값. 내가 봐도 헷갈리게 만들어놨다.. 분리할걸 ㅎㅎ
        comment = get_object_or_404(Comment, id=id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    