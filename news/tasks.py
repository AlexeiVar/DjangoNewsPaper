from django.core.mail import EmailMultiAlternatives
import datetime
from celery import shared_task

from django.template.loader import render_to_string

from .models import Post, Category
from NewsPaper.settings import SITE_URL, DEFAULT_FROM_EMAIL


@shared_task
def send_weekly_mail():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(creation_time__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers_emails = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_message = render_to_string(
        'weekly_mail.html',
        {"link": SITE_URL,
         'posts': posts
         }
    )

    msg = EmailMultiAlternatives(
        subject='Недельные статьи',
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )

    msg.attach_alternative(html_message, 'text/html')
    msg.send()


@shared_task()
def send_notifications(pk):
    post = Post.objects.get(pk=pk)
    title = post.title
    categories = post.category.all()
    emails = []
    for category in categories:
        subscribers = category.subscribers.all()
        for subscriber in subscribers:
            emails.append(subscriber.email)
    html_contect = render_to_string(
        'post_created_letter.html',
        {
            'text': post.preview(),
            'link': f'{SITE_URL}/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=emails,
    )

    msg.attach_alternative(html_contect, 'text/html')
    msg.send()
