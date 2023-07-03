from django import template

register = template.Library()

@register.filter
def sum_prices(products):
    total = sum(product.price for product in products)
    return total