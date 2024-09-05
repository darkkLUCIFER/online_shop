from apps.products.models import Product

CART_SESSION_KEY = 'cart'


class Cart:
    """
        this class handles the user cart methods
    """

    def __init__(self, request):
        self.session = request.session

        cart_sessions = self.session.get(CART_SESSION_KEY)
        if not cart_sessions:
            cart_sessions = self.session[CART_SESSION_KEY] = {}

        self.cart = cart_sessions

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product_name'] = product.name

        for item in cart.values():
            item['total_price'] = int(item['price']) * item['quantity']
            yield item

    @classmethod
    def get_instance(cls, request):
        return Cart(request)

    def save_session(self):
        """
            saves the session object in the session variable
        """
        self.session.modified = True

    def add(self, product, quantity):
        """
            add a product to the cart
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        self.cart[product_id]['quantity'] += quantity
        self.save_session()

    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())
