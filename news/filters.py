from django_filters import FilterSet, DateFilter
from .models import Post
from django import forms


class NewsFilter(FilterSet):
    creation_time = DateFilter(
        field_name='creation_time',
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='date__gte',
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
        }
