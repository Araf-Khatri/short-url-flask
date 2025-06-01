from .public_routes import public_blueprint

def app_routes(app):
  app.register_blueprint(public_blueprint, url_prefix="/v1")