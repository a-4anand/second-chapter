import razorpay
from django.conf import settings

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def create_razorpay_order(amount, currency='INR', receipt='order_rcptid_1'):
    data = {
        "amount": amount * 100,  # Amount in paise
        "currency": currency,
        "receipt": receipt
    }
    order = client.order.create(data=data)
    return order['id']