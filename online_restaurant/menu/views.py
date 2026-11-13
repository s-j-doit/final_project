from django.shortcuts import render
from .models import Dish
from django.views.decorators.cache import never_cache


@never_cache
def dish_list(request):
    dishes = Dish.objects.all()

    # filter by category
    category = request.GET.get('category')
    if category:
        dishes = dishes.filter(category=category)

    # filter by spice level
    spice_level = request.GET.get('spice_level')
    if spice_level in ['0', '1', '2', '3', '4']:
        dishes = dishes.filter(spice_level=int(spice_level))

    # filter by walnuts
    walnuts = request.GET.get('walnuts')
    if walnuts == 'yes':
        dishes = dishes.filter(contains_walnuts=True)
    elif walnuts == 'no':
        dishes = dishes.filter(contains_walnuts=False)

    # filter by vegetarian
    vegetarian = request.GET.get('vegetarian')
    if vegetarian == 'yes':
        dishes = dishes.filter(is_vegetarian=True)
    elif vegetarian == 'no':
        dishes = dishes.filter(is_vegetarian=False)

    context = {
        'dishes': dishes,
        'categories': Dish.Category.choices,
    }

    return render(request, 'menu/dish_list.html', context)
