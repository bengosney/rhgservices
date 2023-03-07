# Django
from django import template

register = template.Library()


@register.filter
def next(some_list, current_index):
    """Returns the next element of the list using the current index if it
    exists."""
    try:
        return some_list[int(current_index) + 1]
    except Exception:
        return None


@register.filter
def previous(some_list, current_index):
    """Returns the previous element of the list using the current index if it
    exists."""
    try:
        return some_list[int(current_index) - 1]
    except Exception:
        return None
