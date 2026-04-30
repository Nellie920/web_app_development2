import os
from flask import Flask
from app.models import db
from app.routes.recipe_routes import recipe_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
    
    # 設定 SQLite 資料庫路徑 (指向 instance/database.db)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 綁定 app 與 db
    db.init_app(app)

    # 註冊 Blueprints
    app.register_blueprint(recipe_bp)

    return app
