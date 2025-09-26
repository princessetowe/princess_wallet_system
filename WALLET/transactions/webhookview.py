import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transactions
import json
import logging
logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class PaystackWebhookView(APIView):
    authentication_classes = [] 
    permission_classes = []

    def post(self, request, *args, **kwargs):
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except Exception as e:
            logger.error(f"Invalid webhook payload: {e}")
            return Response({"error": "Invalid payload"}, status=400)

        logger.info(f"Webhook received: {json.dumps(payload, indent=2)}")

        event = payload.get("event")
        data = payload.get("data", {})
        reference = data.get("reference")

        if not reference:
            logger.warning("No reference in webhook payload")
            return Response({"error": "No reference in payload"}, status=400)

        try:
            transaction = Transactions.objects.get(reference=reference)
        except Transactions.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=404)

        verify_url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        r = requests.get(verify_url, headers=headers).json()
        
        if r.get("status"):
            paystack_status = r["data"]["status"]
            transaction = Transactions.objects.filter(reference=reference).first()
            if transaction:
                transaction.status = "Success" if paystack_status == "success" else "Failed"
                transaction.wallet.balance += transaction.amount if paystack_status == "success" else 0
                transaction.wallet.save()
                transaction.save()

        return Response({"status": "ok"}, status=200)
