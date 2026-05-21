from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), unique=True, nullable=False, index=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(2048))
    category = db.Column(db.String(128))
    is_affiliate = db.Column(db.Boolean, default=False)
    affiliate_url = db.Column(db.String(2048))
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_reviewed_at = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f'<Product {self.id}: {self.title}>'

class PostHistory(db.Model):
    __tablename__ = 'post_histories'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    platform = db.Column(db.String(50), nullable=False)
    post_content = db.Column(db.Text)
    posted_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='success')
    error_message = db.Column(db.Text)

    def __repr__(self):
        return f'<PostHistory {self.id}: {self.platform} ({self.status})>'

class UserPreference(db.Model):
    __tablename__ = 'user_preferences'

    id = db.Column(db.Integer, primary_key=True)
    category_weight = db.Column(db.Text)  # JSON
    liked_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<UserPreference {self.id}>'
