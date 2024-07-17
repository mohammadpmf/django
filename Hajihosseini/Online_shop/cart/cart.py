from products.models import Product

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

    def add(self, product, quantity=1):
        """
        Add the specified product to the cart if it exists
        """
        product_id=str(product.id)
        if product_id not in self.cart:
            self.cart[product_id]={'quantity': quantity}
        else:
            self.cart[product_id]['quantity']+= quantity
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
            self.save()
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product_obj'] = product
        for item in cart.values():
            yield item
    
    def __len__(self):
        return len(self.cart.keys())
    
    def clear(self):
        del self.session['cart']
        self.save()

    def get_total_price(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return sum([product.price for product in products])