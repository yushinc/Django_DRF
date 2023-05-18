from rest_framework import permissions

class CustomReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = GET, 요청 시 true 반환
        if request.method in permissions.SAFE_METHODS:
            return True

        # GET이 아닌 PUT/PATCH 등의 메소드는 요청한 유저와 토큰 유저 비교하여
        # 같으면 true 반환
        return obj.user == request.user
