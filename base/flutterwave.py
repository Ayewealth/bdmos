import requests
import json
from django.conf import settings
import logging
from environ import Env  # type: ignore
env = Env()
Env.read_env()

logger = logging.getLogger(__name__)


def initialize_payment(amount, user, fee_type):
    url = 'https://api.flutterwave.com/v3/payments'
    secret_key = "FLWSECK_TEST-cbaa808bbfac298abb68c210595e2e01-X"
    print(secret_key)
    if not secret_key:
        logger.error(
            "FLUTTERWAVE_SECRET_KEY not found in environment variables.")
        return None, {"message": "Server configuration error: missing payment gateway secret key."}

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {secret_key}'
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
            "title": fee_type.name,
            "description": f"For The Payment Of {fee_type.name}",
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
    secret_key = "FLWSECK_TEST-cbaa808bbfac298abb68c210595e2e01-X"
    if not secret_key:
        logger.error(
            "FLUTTERWAVE_SECRET_KEY not found in environment variables.")
        return None, {"message": "Server configuration error: missing payment gateway secret key."}

    headers = {
        'Authorization': f'Bearer {secret_key}',
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
