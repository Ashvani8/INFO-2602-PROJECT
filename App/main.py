import os
from flask import Flask, render_template
from App.database import init_db
from App.config import load_config
from App.controllers import setup_jwt, add_auth_context
from App.views import views
from App.views.auth import auth_views  # Update the import statement

def add_views(app):
    for view in views:
        app.register_blueprint(view)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static', template_folder='templates')  # Add template_folder parameter
    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    jwt = setup_jwt(app)
    
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
