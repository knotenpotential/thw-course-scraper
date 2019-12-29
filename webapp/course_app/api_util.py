from functools import wraps
from django.http import JsonResponse, HttpResponseForbidden

_VALID_API_KEYS = {"123"}


def is_api_key_valid(api_key):
    return api_key in _VALID_API_KEYS


def validate_api_key(request):
    key = request.META.get("HTTP_X_API_KEY")
    return is_api_key_valid(key)


# Decorator that enforces an API key for the given route. Inspired by the Flask variant:
# https://coderwall.com/p/4qickw/require-an-api-key-for-a-route-in-flask-using-only-a-decorator
# The actual decorator function
def require_api_key(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        request = args[0]
        if validate_api_key(request):
            return view_function(*args, **kwargs)
        else:
            return JsonResponse({
                "success": False,
                "message": "A valid API key must be sent in the X_API_KEY header."
            }, status=HttpResponseForbidden.status_code)

    return decorated_function
