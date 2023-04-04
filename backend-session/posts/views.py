from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Post

def hello_world(request) :
    if request.method == "GET":
        return JsonResponse({
            "status": 200, # 보통 성공했을 때 '200'을 전달.
            "success": True,
            "message": "메시지 전달 성공!",
            "data": "Hello World",
        })
    
def introduction(request) :
    if request.method == "GET":
        return JsonResponse(
        {
            "status": 200, # 보통 성공했을 때 '200'을 전달.
            "success": True,
            "message": "메시지 전달 성공!",
            "data": [
            {
                "name": "민병록",
                "age": 24,
                "major": "CSE"
            },
            {
                "name": "박진영",
                "age": 24,
                "major": "Economics"
            }
        ]})
    
@require_http_methods(["GET"]) #데코레이터
def get_post_detail(request, id):
    post = get_object_or_404(Post, pk = id) #id를 pk로 사용한다. post변수에 해당 id의 wirter, content, category 정보를 넘겨준다. 
    category_json={
        "id": post.id, #primary key
        "writer": post.writer,
        "content": post.content,
        "category": post.category,
    }

    return JsonResponse({
        'status': 200,
        'message': '게시글 조회 성공',
        'data':category_json
    })

@require_http_methods(["GET"]) #데코레이터. 아래 함수를 감싸는 함수로서 여기서는 GET 이외의 요청이 왔을 떄 오류 메시지를 전달한다. 
def get_all_posts(request):
    all_post = Post.objects.all()
    post_list = [] # 공백 리스트를 만들고 append를 통해 id 순서대로 넣어준다. 
    for x in all_post:
        post_info={
        "id": x.id,
        "writer": x.writer,
        "content": x.content,
        "category": x.category,
        }
        post_list.append(post_info)

    return JsonResponse({
        'status': 200,
        'message': '모든 post 게시글 조회 성공',
        'data': post_list # post_info를 담고 있는 post_list를 출력한다. 
    })
