from django.urls import path, include
# Импортируем созданное нами представление
from .views import (
    NewsList, NewsDetail, NewsSearch, NewsCreate, PostCreate, PostUpdate, PostDelete, become_author,
    subscribe, unsubscribe
)

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('search', NewsSearch.as_view(), name='news_search'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('news/create', NewsCreate.as_view(), name='news_create'),
    path('post/create', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('post/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('become_author/', become_author, name='become_author'),
    path('category/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('category/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
]
