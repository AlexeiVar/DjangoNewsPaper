from django.core.management.base import BaseCommand, CommandError
from news.models import Category, Post


class Command(BaseCommand):
    help = 'Удаляет все новости из категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы уверены что хотите удалить все носоти из категории{options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отмена'))
            return
        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Удалены все новости из категории: {category.name}'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Категория: {options["category"]} не найдена'))