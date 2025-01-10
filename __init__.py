from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config['UPLOAD_FOLDER'] = 'user_upload_files'
    
    # Register routes
    from .routes import main
    app.register_blueprint(main)

    return app