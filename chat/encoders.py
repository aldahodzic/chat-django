import json

class DateEncoder(json.JSONEncoder):
  def default(self, obj):
    return obj.timestamp()
