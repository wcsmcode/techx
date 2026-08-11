# cart/cart.py
from decimal import Decimal
from django.conf import settings
from techx.models import ProductVariant

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, variant_id, quantity=1, override_quantity=False):
        variant_id = str(variant_id)
        if variant_id not in self.cart:
            self.cart[variant_id] = {'quantity': 0}
        
        if override_quantity:
            self.cart[variant_id]['quantity'] = quantity
        else:
            self.cart[variant_id]['quantity'] += quantity
        self.save()

    def remove(self, variant_id):
        variant_id = str(variant_id)
        if variant_id in self.cart:
            del self.cart[variant_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        variant_ids = self.cart.keys()
        variants = ProductVariant.objects.filter(id__in=variant_ids).select_related('product')
        
        # Tạo dictionary map id -> object
        variant_map = {str(v.id): v for v in variants}
        
        # Tạo bản sao cart để duyệt
        cart = self.cart.copy()

        for variant_id, item in cart.items():
            # Chỉ yield những item thực sự tồn tại trong DB
            if variant_id in variant_map:
                item['variant'] = variant_map[variant_id]
                item['price'] = Decimal(str(item['variant'].price))
                item['total_price'] = item['price'] * item['quantity']
                yield item
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['variant'].price) * item['quantity'] for item in self.cart.values() if 'variant' in item)

    def clear(self):
        del self.session['cart']
        self.save()