from django.http import HttpResponse
import json

def json_middleware(get_response):

  def middleware(request):

    if (request.method == "POST" or request.method == "PUT"):
      if (request.content_type == "application/json"):
        try:
          request.json = json.loads(request.body)
        except:
          return HttpResponse("Poorly formed JSON.",status=400)
      else:
        return HttpResponse("All POST / PUT requests must use JSON.", status=415)

    return get_response(request)

  return middleware
