from django import template
import datetime
register = template.Library()


def split(strings,key):
    return str(strings).split(key)

register.filter("split",split)