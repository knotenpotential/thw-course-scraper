from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from .repository import upsert_blueprints_from_dict, SUCCESS_CODES, add_new_last_minute_seat_scrape_from_dic, \
    upsert_training_dates_from_dict, get_all_blueprints
from .api_util import require_api_key

# Create your views here.

from django.views.decorators.http import require_http_methods


@require_api_key
@csrf_exempt  # ToDo: Remove this for production when SSL is enabled
@require_http_methods(["POST"])
def add_blueprints(request):
    try:
        # ToDo: Handling for bad requests
        json_data = json.loads(request.body)
        created = upsert_blueprints_from_dict(json_data)
        return JsonResponse({
            "success": created in SUCCESS_CODES,
            "created": created
        })
    except json.decoder.JSONDecodeError as err:
        response = JsonResponse({
            "success": False,
            "message": err.msg},
            status=HttpResponseBadRequest.status_code
        )
        return response


@require_api_key
@csrf_exempt  # ToDo: Remove this for production when SSL is enabled
@require_http_methods(["POST"])
def add_training_dates(request):
    try:
        # ToDo: Handling for bad requests
        json_data = json.loads(request.body)
        created = upsert_training_dates_from_dict(json_data)
        return JsonResponse({
            "success": created in SUCCESS_CODES,
            "created": created
        })
    except json.decoder.JSONDecodeError as err:
        response = JsonResponse({
            "success": False,
            "message": err.msg},
            status=HttpResponseBadRequest.status_code
        )
    return response


@require_api_key
@csrf_exempt  # ToDo: Remove this for production when SSL is enabled
@require_http_methods(["POST"])
def add_scrape(request):
    json_data = json.loads(request.body)
    created = add_new_last_minute_seat_scrape_from_dic(json_data)
    return JsonResponse({
        "success": created in SUCCESS_CODES,
        "created": created
    })


@require_http_methods(["GET"])
def get_training_blueprints(request):
    blueprints = get_all_blueprints()
    return JsonResponse({"blueprints": [blueprint.to_json() for blueprint in blueprints]})
