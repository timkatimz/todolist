from django.urls import path

from goals import views


urlpatterns = [
    path("goal_category/create", views.GoalCategoryCreateView.as_view(), name="category-create"),
    path("goal_category/list", views.GoalCategoryListView.as_view(), name="category-list"),
    path("goal_category/<pk>", views.GoalCategoryView.as_view(), name="category-detail"),

    path("goal/create", views.GoalCreateView.as_view(), name="create-goal"),
    path("goal/list", views.GoalListView.as_view(), name="goal-list"),
    path("goal/<pk>", views.GoalView.as_view(), name="goal-detail"),

    path("goal-comment/create", views.GoalCommentCreateView.as_view(), name="comment-goal"),
    path("goal-comment/list", views.GoalCommentListView.as_view(), name="comment-list"),
    path("goal-comment/<pk>", views.GoalCommentView.as_view(), name="comment-detail"),
]
