from rest_framework import filters


class CurrentUserFollowingFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):

        # Get all the users that the current user is following
        followed_users = [edge.to_user for edge in request.user.profile.following.all()]

        return queryset.filter(author__in=followed_users,is_published=True)
