from flask import Flask
from .routes import app_routes
from .config import Config
from .db import engine
from .db.base import Base

app = Flask(__name__)

app.config.from_object(Config)
Base.metadata.create_all(bind=engine)

app_routes(app)
