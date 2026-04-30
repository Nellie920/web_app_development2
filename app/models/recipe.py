from datetime import datetime
from app.models import db

class Recipe(db.Model):
    """
    食譜 Model
    儲存食譜的基本資訊、材料與步驟
    """
    __tablename__ = 'recipe'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    materials = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 關聯到 Comment (一對多)，刪除食譜時一併刪除相關留言
    comments = db.relationship('Comment', backref='recipe', lazy=True, cascade='all, delete-orphan')
    
    @classmethod
    def get_all(cls):
        """
        取得所有食譜記錄
        回傳依建立時間反向排序的食譜列表
        """
        try:
            return cls.query.order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"Error in get_all: {e}")
            return []

    @classmethod
    def get_by_id(cls, recipe_id):
        """
        取得單筆食譜記錄
        參數:
            recipe_id: 食譜 ID
        回傳 Recipe 物件，若找不到則回傳 None
        """
        try:
            return cls.query.get(recipe_id)
        except Exception as e:
            print(f"Error in get_by_id: {e}")
            return None

    @classmethod
    def create(cls, data):
        """
        新增一筆食譜記錄
        參數:
            data: dict，包含 title, materials, steps, image_path 等資訊
        """
        try:
            new_recipe = cls(**data)
            db.session.add(new_recipe)
            db.session.commit()
            return new_recipe
        except Exception as e:
            db.session.rollback()
            print(f"Error in create: {e}")
            raise e

    def update(self, data):
        """
        更新食譜記錄
        參數:
            data: dict，包含欲更新的欄位與值
        """
        try:
            for key, value in data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error in update: {e}")
            raise e

    def delete(self):
        """
        刪除此筆食譜記錄
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error in delete: {e}")
            raise e


class Comment(db.Model):
    """
    留言 Model
    儲存訪客對於食譜的留言
    """
    __tablename__ = 'comment'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, data):
        """
        新增一筆留言記錄
        參數:
            data: dict，包含 recipe_id, content
        """
        try:
            new_comment = cls(**data)
            db.session.add(new_comment)
            db.session.commit()
            return new_comment
        except Exception as e:
            db.session.rollback()
            print(f"Error in create comment: {e}")
            raise e
