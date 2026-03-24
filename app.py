from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from admin_site.app.routes import main_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'  # Change for production
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    app.register_blueprint(main_bp, url_prefix='/admin')
    
    @app.route('/')
    def index():
        return redirect(url_for('main.inventory_list'))
    
    return app

app = create_app()

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
