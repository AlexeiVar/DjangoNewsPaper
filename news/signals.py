from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from NewsPaper import settings
from .models import PostCategory


# Технически не сигнал, но тут держать его нормально
def send_notifications(preview, pk, title, emails):
    html_contect = render_to_string(
        'post_created_letter.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=emails,
    )

    msg.attach_alternative(html_contect, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_new_post(sender, instance, **kwargs):
    if kwargs['action'] == "post_add":
        categories = instance.category.all()
        subscribers_emails = []
        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [sub.email for sub in subscribers]
        send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)
