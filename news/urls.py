from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, NewsSearch, NewsCreate, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('search', NewsSearch.as_view(), name='news_search'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('news/create', NewsCreate.as_view(), name='news_create'),
    path('post/create', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('post/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_edit'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_edit'),
]
