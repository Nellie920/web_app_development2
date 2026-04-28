from datetime import datetime
from app import db

class Recipe(db.Model):
    __tablename__ = 'recipe'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    materials = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 建立與 Comment 的一對多關聯
    comments = db.relationship('Comment', backref='recipe', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Recipe {self.id}: {self.title}>'
