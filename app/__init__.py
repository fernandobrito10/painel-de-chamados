from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__, 
                template_folder='../templates',  # Especifica o diretório de templates
                static_folder='../static')       # Especifica o diretório de arquivos estáticos
    
    app.config.from_object(Config)

    from app.routes import bp
    app.register_blueprint(bp)

    return app