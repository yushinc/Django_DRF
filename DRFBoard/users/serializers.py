from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from users.models import Profile


# 회원가입 시리얼라이저 선언
class RegisterSerializer(serializers.ModelSerializer):
    # 이메일 필드 (데이터 변환)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())], # 이메일 중복 검증
    )

    # 비밀번호 필드 (데이터 변환)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password], # 비밀번호 검증
    )

    # 비밀번호 확인을 위한 필드 (데이터 변환)
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    # 모델 사용
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    # 비밀번호 일치 여부 검증
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password': "Password fields didn't match."})
        return data

    # 유저 생성
    def create(self, validated_data):
        # 유저 생성
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        # 토큰 생성
        token = Token.objects.create(user=user)
        return user


# 로그인 시리얼라이저 선언
class LoginSerializer(serializers.Serializer):
    # 데이터 변환
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    # 토큰에서 해당 유저 찾아 응답
    def validate(self, data):
        user = authenticate(**data)

        if user:
            token = Token.objects.get(user=user)
            return token

        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials."}
        )

# 프로필 시리얼라이저
class ProfileSerializer(serializers.Serializer):
    class Meta:
        model = Profile
        fields = ("nickname", "position", "subjects", "image")





