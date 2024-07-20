import requests
import json

from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.conf import settings

from orders.models import Order

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10
    # از اینجا به بعد فقط باهاش نوشتم که نمونه داشته باشم. مال ۲ سال پیش بود.
    # احتمال زیاد یو آر ال زرین پال عوض شده و کار نکنه. از طرفی باید کد من هم تایید میشد که
    # نماد اعتماد نگرفتم و تایید نشد و کار نمیکنه. اما با همین وضع دارم کامیت میکنم.
    zarinpal_request_url = 'https://api.zarinpal.com/pg/v4/payment/request.json'
    request_data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': rial_total_price,
        'description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
        'callback_url': '127.0.0.1:8000'
    }
    request_header = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    response = requests.post(zarinpal_request_url, data=json.dumps(request_data), headers=request_header)
    data = response.json()['data']
    authority = data['authority']
    order.zarinpal_authority = authority
    order.save()

    if ('errors' not in data) or (len(response.json()['errors']) == 0):
        return redirect('https://www.zarinpal.com/pg/StartPay/{}' %authority)
    else:
        return HttpResponse("Error from Zarinpal")
