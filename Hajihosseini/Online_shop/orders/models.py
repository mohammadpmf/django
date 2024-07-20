from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _


class Order(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('User'))
    is_paid = models.BooleanField(default=False, verbose_name=_('Is Paid?'))

    first_name = models.CharField(max_length=100, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=100, verbose_name=_('Last Name'))
    phone_number = models.CharField(max_length=15, verbose_name=_('Phone Number'))
    address = models.CharField(max_length=700, verbose_name=_('Address'))
    
    order_notes = models.TextField(max_length=700, blank=True, verbose_name=_('Order Notes'))

    zarinpal_authority = models.CharField(max_length=255, blank=True) # این رو برای ذخیره کد پیگیری زرین پال تعریف کردیم.
    zarinpal_ref_id = models.CharField(max_length=255, blank=True) # این رو برای ذخیره کد پیگیری زرین پال تعریف کردیم.
    zarinpal_data = models.TextField(blank=True)
    
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date Time of creation'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('Date Time of last edit'))

    def __str__(self):
        return f"Order {self.id}"
    
    def get_total_price(self):
        # total_price = 0
        # for item in self.items.all():
        #     item: OrderItem
        #     total_price += item.price*item.quantity
        # return total_price
        return sum(item.price*item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('Order'))
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='order_items', verbose_name=_('Product'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'))
    price = models.PositiveIntegerField(verbose_name=_('Price'))

    def __str__(self):
        return f"OrderItem {self.id}: {self.product} x {self.quantity} Price: {self.price}"
