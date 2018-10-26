from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseForbidden

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
    template_name = 'Article/article_list.html'

    def get_queryset(self):
        queryset = Article.objects.all()
        # search bar ('q' is grabbed from article_list.html)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(ingredient__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query)
            ).distinct()
        return queryset


class ArticleDetailView(DetailView):
    template_name = 'Article/article_detail.html'

    def get_object(self, queryset=None):
        slug_ = self.kwargs.get("slug")
        return get_object_or_404(Article, slug=slug_)

@method_decorator(login_required, name='dispatch')
class ArticleCreateView(CreateView):
    template_name = 'Article/article_create.html'
    form_class = ArticleModelForm
    queryset = Article.objects.all()
    success_url = reverse_lazy('article:article-list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user  # obj.author from author field in the Model
        return super().form_valid(form)


class ArticleUpdateView(AjaxFormMixin, UpdateView):
    template_name = 'Article/article_update.html'
    form_class = ArticleModelForm
    queryset = Article.objects.all()
    model = Article

    def get_success_url(self):
        return reverse('article:article-list')

    def get_object(self, queryset=None):
        slug_ = self.kwargs.get("slug")
        obj = get_object_or_404(Article, slug=slug_)
        # check to see if the user owns the update item
        if not obj.author == self.request.user:
            raise Http404
        return obj

    # def post(self, request, *args, **kwargs):
    #         # the Post object
    #     self.object = self.get_object()
    #     if self.object.author == request.user:
    #         success_url = self.get_success_url()
    #         self.object.save()
    #         return HttpResponseRedirect(success_url)
    #     else:
    #         return HttpResponseForbidden("You are not author of this post. Cannot update other's posts")


class ArticleDeleteView(DeleteView):
    template_name = 'Article/article_delete.html'
    model = Article

    def get_success_url(self):
        return reverse('article:article-list')

    def delete(self, request, *args, **kwargs):
        # the Post object
        self.object = self.get_object()
        if self.object.author == request.user:
            success_url = self.get_success_url()
            self.object.delete()
            return HttpResponseRedirect(success_url)
        else:
            return HttpResponseForbidden("You are not author of this post. Cannot delete other's posts")
