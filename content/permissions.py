from rest_framework import permissions


# TODO: IMPLEMENT PERMISSIONS FOR UPDATING,DELETING POSTS,LIKES,COMMENTS
class IsOwnerOrReadOnlyComment(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # TODO: IMPLEMENT PERMISSIONS REQUIRED FOR PRIVATE PROFILES
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.commented_by == request.user.profile


class IsOwnerOrReadOnlyLike(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # TODO: IMPLEMENT PERMISSIONS REQUIRED FOR PRIVATE PROFILES
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.liked_by == request.user.profile
