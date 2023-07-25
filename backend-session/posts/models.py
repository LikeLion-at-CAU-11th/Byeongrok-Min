from django.db import models
from accounts.models import Member

class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True) # 챌린지 과제: filter orm을 이용하기. 더미데이터를 만들어서 get으로 불러오는데 시간을 조건으로 해서 불러오기. 
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)

    class Meta:
        abstract = True

# Django 모델에서 필드, 즉 칼럼은 하나의 클래스로 생성된다. 
class Post(BaseModel):

    CHOICES = (
        ('DIARY', '일기'),
        ('STUDY', '공부'),
        ('ETC', '기타')
    )
    # 장고 : QuerySet ORM을 이용함. (Object Relational Mapping의 약어로 객체와 db를 매핑.)
    # 장고에서는 스키마 설정을 다르게 했을 때 마이그레이션(migration)으로 업데이트 해줘야 함. 
    id = models.AutoField(primary_key=True)
    # writer = models.CharField(verbose_name="작성자", max_length=30)
    writer = models.ForeignKey(to=Member, on_delete=models.CASCADE) 
    content = models.TextField(verbose_name="내용")
    category = models.CharField(choices=CHOICES, max_length=20)
    # 사용자는 여러 개의 게시글을 작성할 수 있지만, 한 게시글은 한 명의 사용자가 작성

class Comment(BaseModel):
    writer = models.CharField(verbose_name="작성자", max_length=30)
    content = models.CharField(verbose_name="내용", max_length=200)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, blank=False) # 댓글은 일대다 관계이다. comment는 Post를 참조하고 있다. 
