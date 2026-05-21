from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    url = Column(String(2048), unique=True, nullable=False, index=True)
    title = Column(String(256), nullable=False)
    description = Column(Text)
    image_url = Column(String(2048))
    category = Column(String(128))
    is_affiliate = Column(Boolean, default=False)
    affiliate_url = Column(String(2048))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_reviewed_at = Column(DateTime(timezone=True))

    def __repr__(self):
        return f'<Product {self.id}: {self.title}>'

class PostHistory(Base):
    __tablename__ = 'post_histories'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    platform = Column(String(50), nullable=False)
    post_content = Column(Text)
    posted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status = Column(String(20), default='success')
    error_message = Column(Text)

    def __repr__(self):
        return f'<PostHistory {self.id}: {self.platform} ({self.status})>'

class UserPreference(Base):
    __tablename__ = 'user_preferences'

    id = Column(Integer, primary_key=True)
    category_weight = Column(Text)  # JSON
    liked_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<UserPreference {self.id}>'
