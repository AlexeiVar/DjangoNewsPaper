from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy

from .models import Post
from .filters import NewsFilter
from .forms import PostForm


class NewsList(ListView):
    model = Post
    ordering = 'creation_time'
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10


class NewsSearch(ListView):
    model = Post
    ordering = 'creation_time'
    template_name = 'news_search.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = Post.news
        return super().form_valid(form)


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = Post.post
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
