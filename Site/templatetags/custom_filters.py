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
  if value != "None":
    return str(float(value) * 100)
  else:
    return value

# will add a css class to the current filter
@register.filter
def currentFilter(value, arg):
    if value == arg:
        return 'current-filter'

# input: object, string
# get value of key in json data
@register.filter
def get(mapping, key):
  return mapping.get(key, '')

# input: string, int
# output: string
# limits decimal places of argument
@register.filter
def decimalLimit(value, dec=2):
  if value != "None":
    return f"{float(value):.{dec}f}"
  else:
    return value

# input: string
# output: string
# format the string to add commas for every thousand
@register.filter
def commas(value):
  return f"{int(value):,}"
