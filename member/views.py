import razorpay
import json
import hmac
import hashlib

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Payment


# Razorpay client
client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


@login_required
def create_order(request):

    price = settings.MEMBERSHIP_PRICE
    amount_paise = price * 100

    order = client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "payment_capture": 1
    })

    Payment.objects.create(
        user=request.user,
        order_id=order["id"],
        amount=price
    )

    context = {
        "order_id": order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount_paise,
        "price": price
    }

    return render(request, "member/payment.html", context)


@login_required
@csrf_exempt
def verify_payment(request):

    if request.method == "POST":

        data = json.loads(request.body)

        order_id = data.get("razorpay_order_id")
        payment_id = data.get("razorpay_payment_id")
        signature = data.get("razorpay_signature")

        generated_signature = hmac.new(
            bytes(settings.RAZORPAY_KEY_SECRET, 'utf-8'),
            bytes(order_id + "|" + payment_id, 'utf-8'),
            hashlib.sha256
        ).hexdigest()

        if generated_signature == signature:

            try:

                payment = Payment.objects.get(order_id=order_id)

                payment.payment_id = payment_id
                payment.status = "success"
                payment.save()

                # activate membership
                payment.user.membership.activate()

                return JsonResponse({
                    "status": "success"
                })

            except Payment.DoesNotExist:

                return JsonResponse({
                    "status": "payment_not_found"
                })

        else:

            return JsonResponse({
                "status": "signature_verification_failed"
            })

    return JsonResponse({"status": "invalid_request"})


@csrf_exempt
def razorpay_webhook(request):

    body = request.body
    signature = request.headers.get("X-Razorpay-Signature")

    generated_signature = hmac.new(
        bytes(settings.RAZORPAY_WEBHOOK_SECRET, 'utf-8'),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(generated_signature, signature):
        return HttpResponse(status=400)

    data = json.loads(body)
    event = data.get("event")

    if event == "payment.captured":

        entity = data["payload"]["payment"]["entity"]
        order_id = entity["order_id"]

        try:

            payment = Payment.objects.get(order_id=order_id)

            if payment.status != "success":

                payment.status = "success"
                payment.payment_id = entity["id"]
                payment.save()

                payment.user.membership.activate()

        except Payment.DoesNotExist:
            pass

    elif event == "payment.failed":

        entity = data["payload"]["payment"]["entity"]
        order_id = entity["order_id"]

        try:

            payment = Payment.objects.get(order_id=order_id)

            payment.status = "failed"
            payment.save()

        except Payment.DoesNotExist:
            pass

    return HttpResponse(status=200)