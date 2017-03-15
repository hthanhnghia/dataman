from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .key_value_storage import KeyValueStorage, InvalidTimestampException, NotFoundException

storage = KeyValueStorage()

@require_http_methods(["POST"])
@csrf_exempt
def save_value_for_key(request):
    post_data = request.POST
    post_data_keys = list(post_data.keys())
    if len(post_data_keys) == 1:
        key = post_data_keys[0]
        value = post_data.get(key)
        storage.save(key, value)
        return HttpResponse('The data has been added', status=201)
    else:
        return HttpResponse('Invalid request', status=400)

@require_http_methods(["GET"])
def get_value_by_key(request, key):
    timestamp = request.GET.get('timestamp', None)

    try:
        value = storage.get(key, timestamp)
        return HttpResponse(value, status=200)

    except InvalidTimestampException:
        return HttpResponse('Invalid timestamp format - Timestamp must be a float', status=400)

    except NotFoundException:
        return HttpResponse(status=204)
    