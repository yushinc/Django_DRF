from rest_framework import permissions


class CustomReadOnly(permissions.BasePermission):

    # 게시글 조회 : 모든 유저
    # 게시글 작성 : 인증된 유저만
    def has_object_permission(self, request, view):

        if request.method == "GET":
            return True  # 모든 유저 조회 가능

        # POST 요청은 인증된 유저만
        return request.user.is_authenticated

        # 게시글 수정/삭제 : 게시글 작성 유저

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True  # 모든 유저 조회 가능

        # PUT이나 PATCH는 요청한 유저와 접근하려는 객체의 저자가 같다면 true (수정, 삭제 권한)
        return obj.author == request.user