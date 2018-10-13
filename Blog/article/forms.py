from django import forms
from .models import Article


class ArticleModelForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Article's Name"}))

    class Meta:
        model = Article
        fields = [
            'title',
            'ingredient',
            'description',
            'image',
        ]
