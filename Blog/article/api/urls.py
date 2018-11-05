from django.urls import path
from .views import ArticleRUDView, ArticleAPIView

urlpatterns = [
    path('', ArticleAPIView.as_view(), name='article-create'),
    path('<slug>/', ArticleRUDView.as_view(), name='article-rud'),
]