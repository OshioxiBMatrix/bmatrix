from django import template
from django.template.defaultfilters import floatformat

register = template.Library()

@register.filter(name='format_price')
def format_price(value):
    """
    Format a number with dot as thousand separator
    Example: 50000 -> 50.000, 1000000 -> 1.000.000
    """
    if value is None:
        return '0'
    
    try:
        # Convert to integer first to remove any decimal part
        value_int = int(float(value))
        
        # Convert to string
        value_str = str(value_int)
        
        # Format with dot as thousand separator
        result = ''
        for i, char in enumerate(reversed(value_str)):
            if i > 0 and i % 3 == 0:
                result = '.' + result
            result = char + result
        
        return result
    except (ValueError, TypeError):
        return str(value)

@register.filter(name='multiply')
def multiply(value, arg):
    """
    Multiply the value by the argument
    Example: 100|multiply:1.2 -> 120
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return value 