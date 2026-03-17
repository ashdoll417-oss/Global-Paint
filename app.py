from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'  # Change for production
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    @app.route('/')
    def health_check():
        return {'status': 'healthy', 'message': 'Flask app is running!'}, 200
    
    return app

def init_db():
    from app import db, create_app
    app = create_app()
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app = create_app()
    init_db()
    app.run(debug=True)
