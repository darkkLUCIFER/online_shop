from apps.orders.services import Cart


def cart(request):
    """
        this custom context processor return users cart info
    """
    cart_info = Cart.get_instance(request)
    return {
        "cart": cart_info,
    }
