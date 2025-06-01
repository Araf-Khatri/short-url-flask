from flask import jsonify

def success_response(data=None, message="Success", status_code=200):
    """
        maps success response as a json object
    """
    response = {
        "status": "success",
        "message": message,
        "data": data
    }
    return jsonify(response), status_code

def error_response(message="Something went wrong", status_code=400, errors=None):
    """
        maps error response as a json object
    """
    response = {
        "status": "error",
        "message": message,
        "errors": errors
    }
    return jsonify(response), status_code