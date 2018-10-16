from django.urls import path
from .views import (
    ArticleDetailView,
    ArticleListView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
)

app_name = 'article'

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('create/', ArticleCreateView.as_view(), name='article-create'),
    path('<slug>/', ArticleDetailView.as_view(), name='article-detail'),
    path('<slug>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('<slug>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
]
