from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

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
                "major": "Economics"
            },
            {
                "name": "박진영",
                "age": 24,
                "major": "Software"
            }
        ]})
