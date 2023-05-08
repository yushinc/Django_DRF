from rest_framework import serializers
from todo.models import Todo

# 전체 조회 시리얼라이저, 완료 Todo 조회 시리얼라이저
class TodoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'complete', 'important')

# 상세 조회 시리얼라이저, 특정 Todo 완료 시키는 시리얼라이저
class TodoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'created', 'complete', 'important')

# Todo 생성, 수정 시리얼라이저
class TodoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('title', 'description', 'important')



