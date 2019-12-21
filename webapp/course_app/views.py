from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .repository import upsert_blueprint_from_dict, SUCCESS_CODES

# Create your views here.

from django.views.decorators.http import require_http_methods


@csrf_exempt  # ToDo: Remove this for production when SSL is enabled
@require_http_methods(["POST"])
def add_blueprint(request):
    try:
        # ToDo: Handling for bad requests
        json_data = json.loads(request.body)
        created = upsert_blueprint_from_dict(json_data)
        return JsonResponse({
            "success": created in SUCCESS_CODES,
            "created": created
        })
    except json.decoder.JSONDecodeError as err:
        response = JsonResponse({
            "success": False,
            "message": err.msg})
        response.status_code = 422  # Unprocessable Entitys
        return response
