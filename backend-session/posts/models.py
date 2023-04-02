from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)

    class Meta:
        abstract = True

class Post(BaseModel):

    CHOICES = (
        ('DIARY', '일기'),
        ('STUDY', '공부'),
        ('ETC', '기타')
    )
    # 장고 : QuerySet ORM을 이용함. (Object Relational Mapping의 약어로 객체와 db를 매핑.)
    # 장고에서는 스키마 설정을 다르게 했을 때 마이그레이션(migration)으로 업데이트 해줘야 함. 
    id = models.AutoField(primary_key=True)
    writer = models.CharField(verbose_name="작성자", max_length=30)
    content = models.TextField(verbose_name="내용")
    category = models.CharField(choices=CHOICES, max_length=20)

class Comment(BaseModel):
    writer = models.CharField(verbose_name="작성자", max_length=30)
    content = models.CharField(verbose_name="내용", max_length=200)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, blank=False)
