from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, field, value):
    get_params = context['request'].GET.copy()
    get_params[field] = value
    return get_params.urlencode()