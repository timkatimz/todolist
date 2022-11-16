from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission

from goals.models import BoardParticipant, GoalCategory, Goal, Board, GoalComment


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id == request.user.id


class BoardPermission(IsAuthenticated):

    def has_object_permission(self, request, view, obj: Board):
        filters: dict = {'user': request.user, 'board': obj}
        if request.method not in permissions.SAFE_METHODS:
            filters['role'] = BoardParticipant.Role.owner
        return BoardParticipant.objects.filter(**filters).exists()


class GoalCategoryPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj: GoalCategory):
        filters: dict = {'user': request.user, 'board': obj.board}
        if request.method not in permissions.SAFE_METHODS:
            filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        return BoardParticipant.objects.filter(**filters).exists()


class GoalPermission(IsAuthenticated):

    def has_object_permission(self, request, view, obj: Goal):
        filters: dict = {'user': request.user, 'board': obj.category.board}
        if request.method not in permissions.SAFE_METHODS:
            filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        return BoardParticipant.objects.filter(**filters).exists()


class CommentPermission(IsAuthenticated):

    def has_object_permission(self, request, view, obj: GoalComment):
        return any((
                request.method in permissions.SAFE_METHODS,
                obj.user_id == request.user.id
        ))
