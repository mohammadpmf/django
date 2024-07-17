from django.contrib import messages
from products.models import Product
from django.utils.translation import gettext as _

class Cart:
    def __init__(self, request):
        """
        Initialize the cart
        """
        self.request = request
        self.session = request.session # خود جنگو سشن رو میفرسته همراه با رکوئست. ما هم تو هر نمونه از کلاس خودمون ذخیره میکنیم که داشته باشیمش همه جا و هر بار هی ننویسیم self.request.session. جداگانه تو self.session ذخیره اش میکنیم که راحت دسترسی داشته باشیم بهش
        cart = self.session.get('cart') # اول میبینیم که از قبل طرف داخل سشنش کارتی ساخته که پر شده باشه یا نه. اگه باشه که ایف اجرا نمیشه. اگه نباشه یه سبد خرید خالی میسازیم براش
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, replace_current_quantity=False):
        """
        Add the specified product to the cart if it exists
        """
        product_id=str(product.id)
        if product_id not in self.cart: # اگه تو سبد خرید نبود که همین الان اضافه شده. پس اضافه اش میکنیم با مقدار اولیه صفر
            self.cart[product_id]={'quantity': 0}
        if replace_current_quantity: # اگر گفته شده بود که مقدار رو جایگزین کن، یعنی طرف تو صفحه سبد خرید نهایی هست و قبلا این آیتم رو اضافه کرده بود و الان مثلا گفته ۸ تا بشه. پس مقدار جدید باید جایگزین بشه.
            self.cart[product_id]['quantity'] = quantity
            messages.success(self.request, _('Product successfully updated'))
        else: # یعنی طرف تو صفحه خرید نیست. و از توی صفحه محصول گفته ۳ تا مثلا اضافه کن. پس به مقدار قبلیش اضافه میکنیم. که دفعه اول به اضافه ۰ میشه و دفعات بعدی به اضافه مقدار قبلیش
            self.cart[product_id]['quantity'] += quantity
            messages.success(self.request, _('Product successfully added to cart'))
        self.save()

    def save(self):
        """
        Mark session as modified to save changes
        """
        self.session.modified=True

    def remove(self, product):
        """
        Remove a product from the cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            messages.success(self.request, _('Product successfully removed from cart'))
            self.save()
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product_obj'] = product
        for item in cart.values():
            item['total_price'] = item['product_obj'].price * item['quantity']
            yield item
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def clear(self):
        del self.session['cart']
        self.save()

    def get_total_price(self):
        return sum([item['quantity'] * item['product_obj'].price for item in self.cart.values()])