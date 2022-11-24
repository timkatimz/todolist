from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission

from goals.models import BoardParticipant, GoalCategory, Goal, Board, GoalComment


class IsOwnerOrReadOnly(BasePermission):
    """Класс permission"""

    def has_object_permission(self, request, view, obj):
        """Метод дает полные полномочия создателю (доски, категории, цели),
         иначе только SAFE_METHODS('GET', 'HEAD', 'OPTIONS')"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id == request.user.id


class BoardPermission(IsAuthenticated):
    """Класс permission для доски"""

    def has_object_permission(self, request, view, obj: Board):
        """Метод проверяет авторизацию пользователя и 
        Если метод из списка SAFE_METHODS, то метод проверяет, является ли
        пользователь участником доски. Также метод проверяет, является ли
        пользователь создателем доски для редактирования или удаления"""
        filters: dict = {'user': request.user, 'board': obj}
        if request.method not in permissions.SAFE_METHODS:
            filters['role'] = BoardParticipant.Role.owner
        return BoardParticipant.objects.filter(**filters).exists()


class GoalCategoryPermission(IsAuthenticated):
    """Метод проверяет авторизацию пользователя и
        Если метод из списка SAFE_METHODS, то метод проверяет, является ли
        пользователь участником доски. Также метод проверяет, является ли
        пользователь создателем или участником доски с ролью редактор(writer)
        для редактирования или удаления категории"""

    def has_object_permission(self, request, view, obj: GoalCategory):
        filters: dict = {'user': request.user, 'board': obj.board}
        if request.method not in permissions.SAFE_METHODS:
            filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        return BoardParticipant.objects.filter(**filters).exists()


class GoalPermission(IsAuthenticated):
    """Метод проверяет авторизацию пользователя и
            Если метод из списка SAFE_METHODS, то метод проверяет, является ли
            пользователь участником доски. Также метод проверяет, является ли
            пользователь создателем или участником доски с ролью редактор(writer)
            для редактирования или удаления цели"""

    def has_object_permission(self, request, view, obj: Goal):
        filters: dict = {'user': request.user, 'board': obj.category.board}
        if request.method not in permissions.SAFE_METHODS:
            filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        return BoardParticipant.objects.filter(**filters).exists()


class CommentPermission(IsAuthenticated):
    """Метод проверяет авторизацию пользователя и
            что пользователь является создателем комментария"""
    def has_object_permission(self, request, view, obj: GoalComment):
        return any((
            request.method in permissions.SAFE_METHODS,
            obj.user_id == request.user.id
        ))
