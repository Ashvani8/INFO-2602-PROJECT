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
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    add_auth_context(app)
    add_views(app)
    init_db(app)
    setup_jwt(app)

    # Register the auth blueprint with a unique name
    app.register_blueprint(auth_views, name='auth')

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
