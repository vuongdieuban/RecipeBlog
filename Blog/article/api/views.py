from rest_framework import generics, mixins
from django.db.models import Q
from article.models import Article
from .serializers import ArticleSerializer


# Create and List view
class ArticleAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    serializer_class = ArticleSerializer

    # endpoint for this is http://127.0.0.1:8000/api/?q='<look_up>'
    def get_queryset(self):
        qs = Article.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(ingredient__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query)
                ).distinct()
        return qs

    # slug field won't show up in POST since we defined it as read_only_fields in PostSerializer
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# Detail, Update, Delete view
class ArticleRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
