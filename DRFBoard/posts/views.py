from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.models import Post, Comment
from posts.permissions import CustomReadOnly
from posts.serializers import PostSerializer, PostCreateSerializer, CommentSerializer, CommentCreateSerializer
from users.models import Profile


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [CustomReadOnly]
    
    # 필터링 코드
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'likes']

    # 게시글 조회 (전체 목록 or 1개)
    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            # 조회 요청 시 Django -> JSON
            return PostSerializer
        # 조회 요청이 아니라면 생성 JSON -> Django
        return PostCreateSerializer

    # 게시글 생성 (저자와 프로필을 지정해줌)
    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(author=self.request.user, profile=profile)


# 좋아요 기능
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 인증된 유저라면 가능
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk) # 요청 게시글의 pk를 통해 특정 게시글 불러오기

    # 요청한 유저가 게시글의 좋아요 배열에 존재한다면
    if request.user in post.likes.all():
        post.likes.remove(request.user) # 좋아요 취소
    else: # 좋아요 배열에 없다면 (= 좋아요를 누르지 않았다면)
        post.likes.add(request.user) # 좋아요 배열에 유저 추가

    return Response({'status': 'ok'})

# 댓글 기능
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [CustomReadOnly]

    # 댓글 조회 (전체 목록 or 1개)
    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            # 조회 요청 시 Django -> JSON
            return CommentSerializer
        # 조회 요청이 아니라면 생성 JSON -> Django
        return CommentCreateSerializer

    # 댓글 생성 (저자와 프로필을 지정해줌)
    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(author=self.request.user, profile=profile)



