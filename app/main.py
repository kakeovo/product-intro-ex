from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'sqlite:///product_intro_ex.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    from app.models import db, Product, PostHistory, UserPreference

    db.init_app(app)

    from app.routes.api import api
    from app.routes.ui import ui

    app.register_blueprint(api)
    app.register_blueprint(ui)

    with app.app_context():
        db.create_all()

    from app.services.scheduler import start_scheduler
    start_scheduler()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000, host='0.0.0.0')
