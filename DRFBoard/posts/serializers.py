from .models import Post, Comment
from rest_framework import serializers
from users.serializers import ProfileSerializer


# 댓글 모든 필드 직렬화 (Django -> JSON)
class CommentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("pk", "profile", "post", "text")


# 사용자가 입력한 댓글 일부 필드 역직렬화 (JSON -> Django)
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("post", "text")


# 게시글 모든 필드 직렬화 (Django -> JSON)
class PostSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ("pk", "profile", "title", "body", "image", "published_date", "likes", "comments")

# 사용자가 입력한 게시글 일부 필드 역직렬화 (JSON -> Django)
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "category", "body", "image")
