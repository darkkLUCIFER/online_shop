import json
import requests

from django.conf import settings

from apps.orders.models import OrderItem, Order
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
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['total_price'] = int(item['price']) * item['quantity']
            yield item

    def __len__(self):
        return len(self.cart)

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

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save_session()

    def clear(self):
        del self.session[CART_SESSION_KEY]
        self.save_session()


class OrderService:
    """
        handle functions for Order management
    """

    @staticmethod
    def get_instance():
        return OrderService()

    def create(self, cart, order):
        """
            create new Order instance & clear the Cart
        """
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                     quantity=item['quantity'])
        # clean user cart
        cart.clear()


class ZarinpalService:
    """
        handle functions for zarinpal service management
    """

    def __init__(self, request):
        self.request = request

        # check for sandbox mode
        if settings.ZARINPAL_SANDBOX == True:
            sandbox = 'sandbox'
        else:
            sandbox = 'www'

        self.ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
        self.ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
        self.ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

        self.MERCHANT = settings.ZARINPAL_MERCHANT
        self.CallbackURL = settings.ZARINPAL_CALLBACKURL
        self.amount = 0
        self.description = None
        self.phone = request.user.phone_number if hasattr(request.user, 'phone_number') else ''

    @staticmethod
    def get_instance(request):
        return ZarinpalService(request)

    def set_amount(self, amount):
        self.amount = amount
        return self

    def set_description(self, description):
        self.description = description
        return self

    def send_request(self):
        data = {
            "MerchantID": self.MERCHANT,
            "Amount": self.amount,
            "Description": self.description or "No description provided",
            "Phone": self.phone,
            "CallbackURL": self.CallbackURL,
        }
        data = json.dumps(data)

        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        try:
            response = requests.post(self.ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    return {'status': True,
                            'url': self.ZP_API_STARTPAY + str(response['Authority']),
                            'authority': response['Authority']}
                else:
                    return {'status': False,
                            'code': str(response['Status'])}
            else:
                return {'status': False, 'code': f'HTTP {response.status_code}'}

        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}

    def verify(self):
        order_id = self.request.session['order_pay']['order_id']
        order = Order.objects.get(pk=int(order_id))
        authority = self.request.GET.get('Authority')

        data = {
            "MerchantID": self.MERCHANT,
            "Amount": order.get_total_price(),
            "Authority": authority,
        }
        data = json.dumps(data)

        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(self.ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                # change order paid status
                order.paid = True
                order.save()
                return {'status': True, 'RefID': response['RefID']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        else:
            return {'status': False, 'code': f'HTTP {response.status_code}'}
