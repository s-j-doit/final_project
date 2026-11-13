from decimal import Decimal
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from menu.models import Dish
from .models import Cart, CartItem, Order, OrderItem


@login_required
@never_cache
@require_POST
def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        dish=dish
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('dish_list')


@login_required
@never_cache
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    items = list(cart.items.select_related('dish').all())

    total = Decimal('0.00')
    item_count = 0

    for item in items:
        item.subtotal = item.dish.price * item.quantity
        total += item.subtotal
        item_count += item.quantity

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'items': items,
        'total': total,
        'item_count': item_count,
    })


@login_required
@never_cache
@require_POST
def update_cart(request):
    cart = get_object_or_404(Cart, user=request.user)

    cart_items = list(cart.items.all())
    updated_quantities = []

    # Check all quantities before saving any changes.
    for item in cart_items:
        quantity_value = request.POST.get(f'quantity_{item.id}')

        try:
            quantity = int(quantity_value)
        except (ValueError, TypeError):
            messages.error(request, 'Please enter a valid quantity for every dish.')
            return redirect('cart_detail')

        if quantity < 1:
            messages.error(request, 'Quantity must be at least 1.')
            return redirect('cart_detail')

        updated_quantities.append((item, quantity))

    # Save all quantities together.
    with transaction.atomic():
        for item, quantity in updated_quantities:
            item.quantity = quantity
            item.save(update_fields=['quantity'])

    messages.success(request, 'Your cart has been updated.')
    return redirect('cart_detail')


@login_required
@never_cache
@require_POST
def update_cart_item(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        return redirect('cart_detail')

    if quantity >= 1:
        item.quantity = quantity
        item.save()

    return redirect('cart_detail')


@login_required
@never_cache
@require_POST
def remove_cart_item(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    return redirect('cart_detail')


@login_required
@never_cache
@require_POST
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.select_related('dish').all()

    if not items.exists():
        return redirect('cart_detail')

    total = sum(
        (item.dish.price * item.quantity for item in items),
        Decimal('0.00')
    )

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            total=total
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                dish=item.dish,
                dish_name=item.dish.name,
                unit_price=item.dish.price,
                quantity=item.quantity
            )

        items.delete()

    return redirect('order_success', order_id=order.id)


@login_required
@never_cache
def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(request, 'cart/order_success.html', {
        'order': order,
    })
