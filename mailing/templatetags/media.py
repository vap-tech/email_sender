from django import template

register = template.Library()


# Создание фильтра
@register.filter()
def media_path(text):
    if text:
        return f'/media/{text}'
    return '#'
