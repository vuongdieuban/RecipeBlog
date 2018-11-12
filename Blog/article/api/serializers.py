from rest_framework import serializers
from article.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    # author is ForeignKey to user (django user), which has attr username, first_name, last_name
    author_name = serializers.CharField(source='author.username', read_only=True)
    class Meta:
        model = Article
        fields = [
            'id',
            'url',
            'author_name',
            'title',
            'created',
            'description',
            'ingredient',
            'slug',
        ]

        read_only_fields = ['slug', 'id']

    def get_url(self,obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)