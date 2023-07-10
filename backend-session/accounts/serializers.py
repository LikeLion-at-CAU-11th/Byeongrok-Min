# 회원가입(password, username, email, age를 받음)
# username이라고 쓰는 이유가 자동 생성 id와 구분해주기 위함(accounts/models.py에 'AbstractUser'에 username이라고 명시됨)
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from .models import Member

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)

    class Meta:
        model = Member
        fields = ['id', 'password', 'username', 'email', 'age']
            
    def save(self, request):
        member = Member.objects.create(
            # .serializer.validated_data : views.py에서 호출 받으면 검증된 데이터를 응답으로 보내줌
            # "rokany@cau"처럼 올바르지 않은 이메일 형식을 집어넣으면 다음과 같은 json 응답
            # {
            #     "email": [
            #         "Enter a valid email address."
            #     ]
            # }           
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            age = self.validated_data['age'],
        )

        # set_password 함수로 암호화 해줌(비밀번호는 보안성 높임)
        member.set_password(self.validated_data['password'])
        member.save()

        return member

    # 중복 username, email 방지하기 위한 메서드
    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)

        if Member.objects.filter(email=email).exists():
            raise serializers.ValidationError('email already exists') # raise: 수동 예외처리 구문
    
        if Member.objects.filter(username=username).exists():
            raise serializers.ValidationError('username already exists')
        
        return data

# 로그인/로그아웃 구현

class AuthSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    class Meta: 
        model = Member
        fields = ['username', 'password']

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if Member.objects.filter(username=username).exists():
            member = Member.objects.get(username=username)
        
            if not member.check_password(password):
                raise serializers.ValidationError("wrong Password")
        else:
            raise serializers.ValidationError("member accounts not exists")
        
        token = RefreshToken.for_user(member)
        refresh_token = str(token)
        access_token = str(token.access_token)

        data = {
            'member': member,
            'refresh_token': refresh_token,
            'access_token': access_token,
        }

        return data

