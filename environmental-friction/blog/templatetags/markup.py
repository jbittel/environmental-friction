from django import template
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

import markdown


register = template.Library()


@register.filter(is_safe=True)
def markup(value):
    return mark_safe(markdown.markdown(force_text(value), output_format='html5'))
