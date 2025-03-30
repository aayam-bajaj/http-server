from flask import Flask
from flask_mongoengine import MongoEngine
from config import Config

db = MongoEngine()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    from app.routes.api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    return app