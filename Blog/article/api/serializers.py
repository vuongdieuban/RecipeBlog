from rest_framework import serializers
from article.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    # author is ForeignKey to user (django user), which has attr username, first_name, last_name
    author_name = serializers.CharField(source='author.username', read_only=True)
    class Meta:
        model = Article
        fields = [
            'id',
            'author_name',
            'title',
            'created',
            'description',
            'ingredient',
            'slug',
        ]

        read_only_fields = ['slug',]