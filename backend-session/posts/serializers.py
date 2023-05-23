from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post 
        fields = "__all__" # db(즉 모델)의 모든 필드 가져오기
        # fields = ["writer", "content"] # 일부 필드 가져올 때는 스트링 형식으로

# modles.py에서 Comment 불러옴.
class CommentSerializer(serializers.ModelSerializer):
    # Django의 Meta 클래스는 모델 클래스 내에 배치됨.
    # Meta 클래스는 Django의 모델에 취급하는 방법을 변경할 수 있음.
    class Meta:
        model =  Comment
        fields = "__all__"
        
