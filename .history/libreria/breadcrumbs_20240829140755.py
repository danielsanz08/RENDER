from django.urls import reverse
from breadcrumbs

def home_crumb():
    return reverse('home'), 'Inicio'

def category_crumb(category):
    return reverse('category', args=[category.slug]), category.name

def product_crumb(product):
    return reverse('product', args=[product.slug]), product.name

breadcrumbs = Breadcrumbs()
breadcrumbs.add('home', home_crumb)
breadcrumbs.add('category', category_crumb, parent='home')
breadcrumbs.add('product', product_crumb, parent='category')

