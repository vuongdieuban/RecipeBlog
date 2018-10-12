from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import ArticleModelForm
from .models import Article
from .mixins import AjaxFormMixin
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)


class ArticleListView(ListView):
    template_name = 'article/article_list.html'

    def get_queryset(self):
        queryset = Article.objects.all()
        # search bar ('q' is grabbed from article_list.html)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        return queryset


class ArticleDetailView(DetailView):
    template_name = 'article/article_detail.html'

    def get_object(self, queryset=None):
        slug_ = self.kwargs.get("slug")
        return get_object_or_404(Article, slug=slug_)


@method_decorator(login_required, name='dispatch')
class ArticleCreateView(CreateView):
    template_name = 'article/article_create.html'
    form_class = ArticleModelForm
    queryset = Article.objects.all()
    success_url = reverse_lazy('article:article-list')

    def form_valid(self, form):
        return super().form_valid(form)


class ArticleUpdateView(AjaxFormMixin, UpdateView):
    template_name = 'article/article_update.html'
    form_class = ArticleModelForm
    queryset = Article.objects.all()
    success_url = reverse_lazy('article:article-list')

    def get_object(self, queryset=None):
        slug_ = self.kwargs.get("slug")
        return get_object_or_404(Article, slug=slug_)


class ArticleDeleteView(DeleteView):
    template_name = 'article/article_delete.html'

    def get_object(self):
        slug_ = self.kwargs.get("slug")
        return get_object_or_404(Article, slug=slug_)

    def get_success_url(self):
        return reverse('article:article-list')


def test_view(request):
    template_name = 'article/article_test.html'
    context = {}
    return render(request, template_name, context)
