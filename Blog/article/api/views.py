from rest_framework import generics, mixins
from django.db.models import Q
from article.models import Article
from .serializers import ArticleSerializer
from .permissions import IsOwnerOrReadOnly

# Create and List view
class ArticleAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    # endpoint for this is http://127.0.0.1:8000/api/?q=<look_up>
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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # slug field won't show up in POST since we defined it as read_only_fields in PostSerializer
    # this post method is handled by CreateModelMixin, put, patch handled by different mixins
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # pass request from the view to the Serializer
    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}


# Detail, Update, Delete view
class ArticleRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug' #'id' is another choice
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    # pass request from the view to the Serializer
    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}

