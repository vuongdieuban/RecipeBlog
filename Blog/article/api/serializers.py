from rest_framework import serializers
from article.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id',
            'author',
            'title',
            'created',
            'description',
            'ingredient',
            'slug',
        ]

        read_only_fields = ['slug', 'author',]