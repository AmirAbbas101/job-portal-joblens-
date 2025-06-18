from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Subscriber
import json


@csrf_exempt  # for simplicity in development; remove if using AJAX with CSRF token
def subscribe_newsletter(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            if not email:
                return JsonResponse(
                    {"success": False, "message": "Email is required."}, status=400
                )

            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse(
                    {"success": False, "message": "Email already subscribed."},
                    status=200,
                )

            Subscriber.objects.create(email=email)
            return JsonResponse(
                {"success": True, "message": "Successfully subscribed!"}, status=201
            )

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse(
        {"success": False, "message": "Invalid request method."}, status=405
    )
