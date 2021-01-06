from django import template
register = template.Library()
from base.models import Category, MenuItem, Cart
from user.models import CustomUser
from django.db.models import Q

@register.simple_tag()
def menu_item(param):
    category_obj = Category.objects.get(category_title=param)
    items = MenuItem.objects.filter(category=category_obj)
    return items


@register.simple_tag()
def multiply_qty_price(price, quantity):
    value = price * quantity
    return value


@register.simple_tag()
def get_stars_range(param):
    return range(0,param)


@register.simple_tag()
def return_true_false(user_id, menu_id):
    item = MenuItem.objects.get(id=menu_id)
    
    try:
        user = CustomUser.objects.get(id=user_id)
        user_cart_obj = Cart.objects.get(Q(user=user) & Q(item=item))
        return True
    except:
        return False


@register.simple_tag()
def return_quantity(user_id, menu_id):
    item = MenuItem.objects.get(id=menu_id)
    user = CustomUser.objects.get(id=user_id)        
    user_cart_obj = Cart.objects.get(Q(user=user) & Q(item=item))
    return user_cart_obj.quantity