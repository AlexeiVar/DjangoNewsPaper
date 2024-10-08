from django.urls import path, include
# Импортируем созданное нами представление
from .views import (
    NewsList, NewsDetail, NewsSearch, NewsCreate, PostCreate, PostUpdate, PostDelete, become_author,
    subscribe, unsubscribe
)
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(30)(NewsList.as_view()), name='news_list'),
    path('search', cache_page(60)(NewsSearch.as_view()), name='news_search'),
    path('<int:pk>', cache_page(60 * 5)(NewsDetail.as_view()), name='news_detail'),
    path('news/create', NewsCreate.as_view(), name='news_create'),
    path('post/create', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('post/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('become_author/', become_author, name='become_author'),
    path('category/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('category/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
    path('i18n/', include('django.conf.urls.i18n')),
]
