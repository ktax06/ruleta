import os
import logging
from flask import Flask
from .router import init_bp

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_key'),
        DATABASE_URL=os.environ.get('DATABASE_URL')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(), 
            logging.FileHandler(os.path.join(app.instance_path, 'app.log')) 
        ]
    )
    
    app.register_blueprint(init_bp, url_prefix='/')

    return app
