from rest_framework import serializers
from .models import Post, Comment

import boto3
from config.settings import AWS_ACCESS_KEY_ID, AWS_REGION, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
VALID_IMAGE_EXTENSIONS = [ "jpg", "jpeg", "png", "gif", ]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post 
        fields = "__all__" # db(즉 모델)의 모든 필드 가져오기
        # fields = ["writer", "content"] # 일부 필드 가져올 때는 스트링 형식으로

        def validate(self, data): 
            image = data.get('thumbnail')

            if not image.name.split('.')[-1].lower() in VALID_IMAGE_EXTENSIONS:
                serializers.ValidationError("Not an Image File")
            s3 = boto3.client('s3',
                aws_access_key_id = AWS_ACCESS_KEY_ID,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
                region_name = AWS_REGION)
            try:
                s3.upload_fileobj(image, AWS_STORAGE_BUCKET_NAME, image.name)
                img_url = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{image.name}"
                data['thumbnail'] = img_url
                return data
            except:
                raise serializers.ValidationError("InValid Image File")

# modles.py에서 Comment 불러옴.
class CommentSerializer(serializers.ModelSerializer):
    # Django의 Meta 클래스는 모델 클래스 내에 배치됨.
    # Meta 클래스는 Django의 모델에 취급하는 방법을 변경할 수 있음.
    class Meta:
        model =  Comment
        fields = "__all__"
        
