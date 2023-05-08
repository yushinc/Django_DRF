from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from todo.models import Todo
from todo.serializers import TodoSimpleSerializer, TodoDetailSerializer, TodoCreateSerializer


# Create your views here.
class TodosAPIView(APIView):
    # 전체 조회
    def get(self, request):
        todos = Todo.objects.filter(complete=False) # 미완료 todo 필터링하여 todos 객체에 저장
        serializer = TodoSimpleSerializer(todos, many=True) # 시리얼라이저를 통해 파이썬 객체 -> 문자열 변환
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Todo 생성
    def post(self, request):
        serializer = TodoCreateSerializer(data=request.data) # 문자열 -> 파이썬 객체 변환
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TodoAPIView(APIView):
    # 상세 조회
    def get(self, request, pk):
        todo = get_object_or_404(Todo, id=pk)
        serializer = TodoDetailSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Todo 수정
    def put(self, request, pk):
        todo = get_object_or_404(Todo, id=pk)
        serializer = TodoCreateSerializer(todo, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

# 완료 목록 조회
class DoneTodosAPIView(APIView):
    def get(self, request):
        dones = Todo.objects.filter(complete=True)
        serializer = TodoSimpleSerializer(dones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 특정 Todo 완료 시키기
class DoneTodoAPIView(APIView):
    def get(self, request, pk):
        done = get_object_or_404(Todo, id=pk)
        done.complete = True # 완료 필드를 True로 변경
        done.save()
        serializer = TodoDetailSerializer(done)
        return Response(status=status.HTTP_200_OK)