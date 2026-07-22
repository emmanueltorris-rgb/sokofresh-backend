import re

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import MpesaTransaction
from .mpesa import MpesaClient
from apps.marketplace.models import Order
from apps.accounts.permissions import IsBuyer, IsVerifiedUser


def normalize_mpesa_phone(phone):
    if not phone:
        return None
    digits = re.sub(r'\D', '', str(phone))
    if digits.startswith('254') and len(digits) == 12:
        return digits
    if digits.startswith('0') and len(digits) == 10:
        return f'254{digits[1:]}'
    if digits.startswith('7') and len(digits) == 9:
        return f'254{digits}'
    if digits.startswith('2540') and len(digits) == 13:
        return digits[1:]
    return None


class MpesaSTKPushView(APIView):
    permission_classes = [IsBuyer, IsVerifiedUser]

    def post(self, request):
        order_id = request.data.get('order_id')
        phone_number = request.data.get('phone_number')
        normalized_phone = normalize_mpesa_phone(phone_number)

        if not normalized_phone:
            return Response(
                {'error': 'Invalid phone_number format. Use 2547XXXXXXXX or 2541XXXXXXXX.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            order = Order.objects.get(id=order_id, buyer=request.user, status='PENDING')
        except Order.DoesNotExist:
            return Response({'error': 'Order not found or not payable.'}, status=status.HTTP_404_NOT_FOUND)

        if not settings.MPESA_CONFIG.get('CALLBACK_URL'):
            return Response(
                {'error': 'MPESA callback URL is not configured.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        mpesa = MpesaClient()
        response = mpesa.stk_push(
            phone_number=normalized_phone,
            amount=int(order.total_amount),
            account_reference=f"Order-{order.order_number}",
            transaction_desc="SokoFresh Produce Purchase",
            callback_url=settings.MPESA_CONFIG['CALLBACK_URL'],
        )

        if response.get('ResponseCode') == '0':
            transaction = MpesaTransaction.objects.create(
                user=request.user,
                order=order,
                merchant_request_id=response.get('MerchantRequestID', ''),
                checkout_request_id=response.get('CheckoutRequestID', ''),
                amount=order.total_amount,
                phone_number=normalized_phone,
            )
            return Response(
                {
                    'message': 'STK Push sent successfully',
                    'checkout_request_id': response.get('CheckoutRequestID'),
                    'transaction_id': transaction.id,
                }
            )

        return Response(
            {'error': response.get('errorMessage', 'Payment initiation failed')},
            status=status.HTTP_400_BAD_REQUEST,
        )


class MpesaCallbackView(APIView):
    permission_classes = []

    def post(self, request):
        data = request.data
        body = data.get('Body', {}).get('stkCallback', {})

        checkout_request_id = body.get('CheckoutRequestID')
        result_code = body.get('ResultCode')
        result_desc = body.get('ResultDesc')

        transaction = get_object_or_404(MpesaTransaction, checkout_request_id=checkout_request_id)

        callback_metadata = body.get('CallbackMetadata', {}).get('Item', [])
        metadata = {item.get('Name'): item.get('Value') for item in callback_metadata}

        transaction.result_code = str(result_code)
        transaction.result_desc = result_desc or ''
        transaction.mpesa_receipt_number = metadata.get('MpesaReceiptNumber', '')
        transaction.transaction_date = str(metadata.get('TransactionDate', ''))

        if result_code == 0:
            transaction.status = 'SUCCESS'
            if transaction.order:
                transaction.order.status = 'PAID'
                transaction.order.save()
        else:
            transaction.status = 'FAILED' if str(result_code) != '103' else 'CANCELLED'
            if transaction.order:
                transaction.order.status = transaction.status
                transaction.order.save()

        transaction.save()

        return Response(
            {
                'message': 'Callback processed',
                'receipt': {
                    'mpesa_receipt_number': transaction.mpesa_receipt_number,
                    'transaction_date': transaction.transaction_date,
                    'amount': str(transaction.amount),
                    'status': transaction.status,
                },
            }
        )
