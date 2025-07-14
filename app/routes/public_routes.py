from flask import Blueprint
from sqlalchemy import select, delete
from ..db.models import Url
from ..db import db
from ..kazoo import counter
from ..utils.response_mapper import success_response, error_response
from ..utils.create_short_url import create_short_url
from ..utils.request_mapper import post_request_mapper

public_blueprint = Blueprint("public", __name__)

@public_blueprint.route("/generate-short-url", methods=["POST"])
@post_request_mapper
def generate_short_url(data):
  try:
    long_url = data["long_url"] or None
    if not long_url:
      return error_response("Url must be present", 400)
    elif not long_url.startswith("https://"):
      return error_response("Please add valid & secure url.", 400)
    
    number = counter.get_number_from_range()
    if not number:
      raise Exception("Unique number not found!")
    print(number)
    short_url = create_short_url(number)
    
    record = Url(short_url=short_url, long_url=long_url, base10_integer=number)
    url = record.to_dict()
    db.add(record)
    db.commit()

    return success_response(url)
  except:
    return error_response("Internal server error", 500)

@public_blueprint.route("/long-url", methods=["GET"])
def get_long_url():
  return success_response()


@public_blueprint.route("/urls", methods=["GET"])
def get_all_urls():
  results = db.execute(select(Url))
  records = results.scalars().all()
  
  records_dict = list(map(lambda x: x.to_dict(), records))
  return success_response(records_dict)

@public_blueprint.route("/urls", methods=["DELETE"])
def delete_url_record():
  db.execute(delete(Url))
  return success_response()

# Step 1: connect with sql
# Step 2: create schema { short_url: string; long_url: string; expires_at: date; created_at: date }
# step 3: 
# CREATE TABLE urls (
# id SERIAL PRIMARY KEY,
# long_url TEXT NOT NULL,
# short_url VARCHAR(20) NOT NULL UNIQUE,
# created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
# expires_at TIMESTAMP,
# );