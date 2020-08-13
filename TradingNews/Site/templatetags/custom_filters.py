from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='format')
def format(value):
    value = value.replace('Z', '')
    value = value.replace('T', ' ')
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

# format decimal number to it's percentage equivalent
@register.filter
def percentage(value):
    return str(float(value) * 100) + "%"

