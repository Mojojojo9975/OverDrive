from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from orders.models import Order
from datetime import datetime, timedelta
import hmac
import hashlib

JAZZCASH_MERCHANT_ID= settings.JAZZCASH_MERCHANT_ID
JAZZCASH_PASSWORD=settings.JAZZCASH_PASSWORD
JAZZCASH_INTEGRITY_SALT=settings.JAZZCASH_INTEGRITY_SALT
# Create your views here.

def payment_process(request):

    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    current_datetime = datetime.now()
    pp_TxnDateTime = current_datetime.strftime('%Y%m%d%H%M%S')
    expiry_datetime = current_datetime + timedelta(hours=1)
    pp_TxnExpiryDateTime = expiry_datetime.strftime('%Y%m%d%H%M%S')
    pp_TxnRefNo = "T" + pp_TxnDateTime + str(order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(
        reverse('payment:completed')
        )
        cancel_url = request.build_absolute_uri(
        reverse('payment:canceled')
        )
   
        session_data={
        "pp_Version": "1.0",
        "pp_TxnType": "",
        "pp_Language": "EN",
        "pp_MerchantID": JAZZCASH_MERCHANT_ID,
        "pp_SubMerchantID": "",
        "pp_Password": JAZZCASH_PASSWORD,
        "pp_BankID": "",
        "pp_ProductID": "",
        "pp_TxnRefNo": pp_TxnRefNo,
        "pp_Amount": 12345678,
        "pp_TxnCurrency": "PKR",
        "pp_TxnDateTime": pp_TxnDateTime,
        "pp_BillReference": "billRef",
        "pp_Description": "Description of transaction",
        "pp_TxnExpiryDateTime": pp_TxnExpiryDateTime,
        "pp_ReturnURL": "The URL where merchant wants the transaction results to be shown. Once the transaction has been processed, response details will be sent over to the merchant on this URL using an HTTP POST Request.",
        "pp_SecureHash": "" ,
        "ppmpf_1": "1",
        "ppmpf_2": "2",
        "ppmpf_3": "3",
        "ppmpf_4": "4",
        "ppmpf_5": "5"
    }
    
        sorted_string = "&".join(f"{key}={value}" for key , value in sorted(session_data.items()) if value != "")
        pp_SecureHash = hmac.new(
            JAZZCASH_INTEGRITY_SALT.encode(),
            sorted_string.encode(),
            hashlib.sha256
        ).hexdigest()
        session_data['pp_SecureHash'] = pp_SecureHash

    else:
        return render(request, 'payment/process.html', locals())


def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/cancelled.html')