from django import template

register = template.Library()

@register.filter(name='count_words')
def count_words(value: str):
    return len(value.split())

@register.filter(name='count_something')
def count_something(value: str, arg: str):
    number = value.count(arg)
    return number

@register.filter(name='remove_brs')
def remove_brs(value: str):
    return value.replace('<br>', '')
