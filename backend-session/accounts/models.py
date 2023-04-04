from django.db import models
from django.contrib.auth.models import AbstractUser 
# 그냥 User가 아닌 AbstactUser를 이용해 기본 유저에 필드를 추가할 수 있다. 

class Member(AbstractUser):
    age = models.IntegerField(verbose_name="나이",default=20, null=True) # verbose_name은 필수는 아니지만 가독성을 위해 명시해주면 좋다. 
    #기본 모델을 상속하고 age 필드를 추가함. 
    # null = True --> 사용자 입력이 필수는 아님. 
    # char 필드 속성을 사용하려면 max_length 지정해줘야 한다. 
