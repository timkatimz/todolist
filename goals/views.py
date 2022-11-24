from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, GoalComment, Board
from goals.permissions import BoardPermission, GoalCategoryPermission, IsOwnerOrReadOnly, GoalPermission, \
    CommentPermission
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, \
    GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer, BoardCreateSerializer, BoardSerializer, \
    BoardListSerializer


class GoalCategoryCreateView(CreateAPIView):
    """Ручка для создания категории"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    """Ручка для отображения списка категорий к которым у пользователя есть доступ"""
    model = GoalCategory
    permission_classes = [GoalCategoryPermission]
    serializer_class = GoalCategorySerializer
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    filterset_fields = ['board']
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        """Метод возвращает из базы queryset списка категорий к которым у пользователя есть доступ"""
        return GoalCategory.objects.prefetch_related('board__participants').filter(
            board__participants__user_id=self.request.user.id, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """Ручка для отображения, редактирования и удаления категории к которым у пользователя есть доступ"""
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermission, IsOwnerOrReadOnly]

    def get_queryset(self):
        """Метод возвращает из базы queryset категории к которым у пользователя есть доступ"""
        return GoalCategory.objects.prefetch_related('board__participants').filter(
            board__participants__user_id=self.request.user.id, is_deleted=False
        )

    def perform_destroy(self, instance: GoalCategory):
        """Метод удаляет категорию, а у всех целей в этой категории меняет статус на архивный"""
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            Goal.objects.filter(category=instance).update(status=Goal.Status.archived)
        return instance


class GoalCreateView(CreateAPIView):
    """Ручка для создания цели"""
    permission_classes = [GoalPermission]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    """Ручка для отображения списка целей"""
    model = Goal
    permission_classes = [GoalPermission]
    serializer_class = GoalSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = GoalDateFilter
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        """Метод возвращает из базы queryset списка целей к которым у пользователя есть доступ"""
        return Goal.objects.select_related('user', 'category__board').filter(
            Q(category__board__participants__user_id=self.request.user.id) & ~Q(status=Goal.Status.archived)
        )


class GoalView(RetrieveUpdateDestroyAPIView):
    """Ручка для отображения, редактирования и удаления цели к которым у пользователя есть доступ"""
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [GoalPermission, IsOwnerOrReadOnly]

    def get_queryset(self):
        """Метод возвращает из базы queryset цели к которому у пользователя есть доступ"""
        return Goal.objects.select_related('user', 'category__board').filter(
            Q(category__board__participants__user_id=self.request.user.id) & ~Q(status=Goal.Status.archived)
        )

    def perform_destroy(self, instance: Goal):
        """Метод меняет статус цели как архивный"""
        instance.status = Goal.Status.archived
        instance.save(update_fields=('status',))
        return instance


class GoalCommentCreateView(CreateAPIView):
    """Ручка для создания комментария"""
    permission_classes = [CommentPermission]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    """Ручка для отображения списка комментариев к которым у пользователя есть доступ"""
    model = GoalComment
    permission_classes = [CommentPermission]
    serializer_class = GoalCommentSerializer
    filter_backends = [OrderingFilter]
    filterset_fields = ["goal"]
    ordering = ["-created"]

    def get_queryset(self):
        """Метод возвращает из базы queryset списка комментариев к которым у пользователя есть доступ"""
        return GoalComment.objects.select_related('goal__category__board', 'user').filter(
            goal__category__board__participants__user_id=self.request.user.id
        )


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    """Ручка для отображения, редактирования и удаления комментария к которым у пользователя есть доступ"""
    model = GoalComment
    permission_classes = [CommentPermission, IsOwnerOrReadOnly]
    serializer_class = GoalCommentSerializer

    def get_queryset(self):
        """Метод возвращает из базы queryset комментария к которому у пользователя есть доступ"""
        return GoalComment.objects.select_related('goal__category__board', 'user').filter(
            goal__category__board__participants__user_id=self.request.user.id
        )


class BoardCreateView(CreateAPIView):
    """Ручка для создания доски"""
    permission_classes = [BoardPermission]
    serializer_class = BoardCreateSerializer


class BoardListView(ListAPIView):
    """Ручка для отображения списка досок к которым у пользователя есть доступ"""
    model = Board
    permission_classes = [BoardPermission]
    serializer_class = BoardListSerializer
    ordering = ["title"]

    def get_queryset(self):
        """Метод возвращает из базы queryset списка досок к которым у пользователя есть доступ"""
        return Board.objects.prefetch_related('participants').filter(
            participants__user__id=self.request.user.id, is_deleted=False)


class BoardView(RetrieveUpdateDestroyAPIView):
    """Ручка для отображения, редактирования и удаления доски к которой у пользователя есть доступ"""
    model = Board
    permission_classes = [BoardPermission]
    serializer_class = BoardSerializer

    def get_queryset(self):
        """Метод возвращает из базы queryset доски к которой у пользователя есть доступ"""
        return Board.objects.prefetch_related('participants').filter(
            participants__user__id=self.request.user.id, is_deleted=False)

    def perform_destroy(self, instance):
        """Метод удаляет доску, и все категории и цели в ней"""
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=['is_deleted'])
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)
        return instance
