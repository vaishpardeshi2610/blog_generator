from flask import Flask
from .routes import init_routes

def create_app():
    app = Flask(__name__)
    
    # Initialize routes
    init_routes(app)
    
    return app