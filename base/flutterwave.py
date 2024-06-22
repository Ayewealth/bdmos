import requests
import json
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def initialize_payment(amount, user, fee_type):
    url = 'https://api.flutterwave.com/v3/payments'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer FLWSECK_TEST-d5f7e4a194af09f6158620240649a49b-X'
    }

    data = json.dumps({
        "tx_ref": f"{user.username}-{amount}",
        "amount": amount,
        "currency": "NGN",
        "redirect_url": "https://bdmos.onrender.com/api/payments-callback/",
        "payment_options": "card, banktransfer, ussd",
        "customer": {
            "email": user.parents_email,
            "phonenumber": user.parents_phone_number,
            "name": f"{user.first_name} {user.last_name}"
        },
        "customizations": {
            "title": fee_type,
            "description": f"For The Payment Of {fee_type}",
            "logo": "https://checkout.flutterwave.com/assets/img/rave-logo.png"
        }
    })

    response = requests.post(url, headers=headers, data=data)
    print(response.text)

    try:
        response_data = response.json()
    except ValueError as e:
        logger.error(f"JSON decode error: {e}")
        logger.error(f"Response content: {response.content}")
        response_data = None

    return response, response_data


def verify_payment(transaction_id):
    url = f'https://api.flutterwave.com/v3/transactions/{transaction_id}/verify'
    headers = {
        'Authorization': f'Bearer FLWSECK_TEST-d5f7e4a194af09f6158620240649a49b-X',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"Error {response.status_code}: {response.content}")

    try:
        response_data = response.json()
    except ValueError as e:
        logger.error(f"JSON decode error: {e}")
        logger.error(f"Response content: {response.content}")
        response_data = None

    return response, response_data
