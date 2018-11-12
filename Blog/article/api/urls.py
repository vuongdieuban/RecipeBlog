from django.urls import path
from .views import ArticleRUDView, ArticleAPIView

app_name = 'article-api'

urlpatterns = [
    path('', ArticleAPIView.as_view(), name='article-listcreate'),
    path('<slug>/', ArticleRUDView.as_view(), name='article-rud'),
]