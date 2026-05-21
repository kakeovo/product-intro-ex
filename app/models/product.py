from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, URL

class Product:
    """商品モデル"""
    id = Column(Integer, primary_key=True)
    url = Column(String(2048), unique=True, nullable=False)
    title = Column(String(256), nullable=False)
    description = Column(Text)
    image_url = Column(String(2048))
    category = Column(String(128))
    is_affiliate = Column(Boolean, default=False)
    affiliate_url = Column(String(2048))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_reviewed_at = Column(DateTime)
