import requests
import base64
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class MpesaClient:
    def __init__(self):
        self.config = settings.MPESA_CONFIG
        self.base_url = (
            "https://sandbox.safaricom.co.ke"
            if self.config['ENVIRONMENT'] == 'sandbox'
            else "https://api.safaricom.co.ke"
        )

    def get_access_token(self):
        consumer_key = self.config.get('CONSUMER_KEY')
        consumer_secret = self.config.get('CONSUMER_SECRET')
        if not consumer_key or not consumer_secret:
            raise ImproperlyConfigured('Missing MPESA_CONSUMER_KEY or MPESA_CONSUMER_SECRET')

        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        credentials = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()
        response = requests.get(url, headers={'Authorization': f'Basic {credentials}'})
        token = response.json().get('access_token')
        if not token:
            raise ImproperlyConfigured('Unable to fetch MPESA access token')
        return token

    def stk_push(self, phone_number, amount, account_reference, transaction_desc, callback_url):
        access_token = self.get_access_token()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(
            f"{self.config['BUSINESS_SHORT_CODE']}{self.config['PASSKEY']}{timestamp}".encode()
        ).decode()

        payload = {
            'BusinessShortCode': self.config['BUSINESS_SHORT_CODE'],
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': self.config['TRANSACTION_TYPE'],
            'Amount': int(amount),
            'PartyA': phone_number,
            'PartyB': self.config['BUSINESS_SHORT_CODE'],
            'PhoneNumber': phone_number,
            'CallBackURL': callback_url,
            'AccountReference': account_reference,
            'TransactionDesc': transaction_desc,
        }

        url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        response = requests.post(
            url,
            json=payload,
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
            },
            timeout=30,
        )
        return response.json()