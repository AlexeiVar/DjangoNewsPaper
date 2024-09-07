from datetime import timedelta, datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.cache import cache_page
from django.utils import timezone
from .models import Post, Category, Author
from .filters import NewsFilter
from .forms import PostForm
from .tasks import send_notifications
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
import pytz


class NewsList(ListView):
    model = Post
    ordering = 'creation_time'
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return HttpResponseRedirect(request.path_info)


class NewsSearch(ListView):
    model = Post
    ordering = 'creation_time'
    template_name = 'news/news_search.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return HttpResponseRedirect(request.path_info)


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'news_detail'

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return HttpResponseRedirect(request.path_info)


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/news_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.author = Author.objects.filter(user=self.request.user)[0]
        form.instance.author = self.request.user.author
        today = datetime.now()
        limit = today - timedelta(days=1)
        count = Post.objects.filter(author=news.author, creation_time__gte=limit).count()
        if count >= 3:
            return render(self.request, 'news/news_limit_reached.html')
        news.type = Post.news
        news.save()
        send_notifications.delay(news.pk)
        return super().form_valid(form)

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return HttpResponseRedirect(request.path_info)


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/news_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.author = Author.objects.filter(user=self.request.user)[0]
        form.instance.author = self.request.user.author
        today = datetime.now()
        limit = today - timedelta(days=1)
        count = Post.objects.filter(author=news.author, creation_time__gte=limit).count()
        if count >= 3:
            return render(self.request, 'news/news_limit_reached.html')
        news.type = Post.post
        news.save()
        send_notifications.delay(news.pk)
        return super().form_valid(form)

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return HttpResponseRedirect(request.path_info)


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/news_create.html'

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return HttpResponseRedirect(request.path_info)


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return HttpResponseRedirect(request.path_info)


@login_required
def become_author(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('/')


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    return_path = request.META.get('HTTP_REFERER', '/')
    return redirect(return_path)


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    return_path = request.META.get('HTTP_REFERER', '/')
    return redirect(return_path)
