from flask import request
from functools import wraps
from .response_mapper import error_response

def post_request_mapper(function):
  @wraps(function)
  def validator(*args, **kwargs):
    if (request.is_json):
      data = request.get_json(force=True)
      return function(data)
    else:
      return error_response("Request body must be a JSON object!", 400)
  
  return validator
