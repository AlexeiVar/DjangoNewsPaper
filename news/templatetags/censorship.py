from django import template
import re

register = template.Library()
# Лист слов которые цензуруются, взяты слова, которые генерировались случайным генератором для примера
black_list = ['bacon', 'ipsum', 'burgdoggen', 'Swine']
# Лист пунктуаций, чтобы можно было убрать пробел перед ними
punctuations = [',', '.', '!', '?']
# Лист соединителей, чтобы такие слова как t-bone могли быть вместе
connectors = ['-']


@register.filter()
def censor(value):
    # Используем прекрасную библиотеку re, чтобы получить пунктуацию и слова отдельно
    processed = re.findall(r'\w+|[^\s\w]+', value)
    result = ''
    for word in processed:
        # Проверяем запрещено ли слово
        if word.lower() in black_list:
            letters = list(word)
            for i in range(len(letters) - 1):
                letters[i + 1] = '*'
            s = ''.join(letters)
            result += f'{s} '
        # Проверяем смотрим ли мы на пунктуацию
        elif word in punctuations:
            result = result.strip()
            result += f'{word} '
        # Проверяем смотрим ли мы на коннектора
        elif word in connectors:
            result = result.strip()
            result += f'{word}'
        # Если ничего не подошло, то это просто обычное слово
        else:
            result += f"{word} "
    result = result.strip()
    return result
