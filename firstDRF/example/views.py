from rest_framework import status, mixins, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from example.models import Book
from example.serializers import BookSerializer


# FBV
@api_view(['GET'])
def HelloAPI(request):
    return Response("hello world")

@api_view(['GET', 'POST'])
def booksAPI(request):
    # 도서 전체 조회
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # 도서 정보 생성
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
# 도서 1권 조회
@api_view(['GET'])
def bookAPI(request, bid):
    book = get_object_or_404(Book, bid=bid)
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)


# CBV
class BooksAPIMixins(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # 도서 전체 조회
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    # 도서 정보 생성
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# mixin
class BookAPIMixins(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid'

    # 도서 1권 조회
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # 도서 1권 수정
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # 도서 1권 삭제
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# generics
class BooksAPIGenerics(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookAPIGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid'

# ViewSet
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer