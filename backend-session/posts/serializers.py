from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post 
        fields = "__all__" # db(즉 모델)의 모든 필드 가져오기
        # fields = ["writer", "content"] # 일부 필드 가져올 때는 스트링 형식으로
        
