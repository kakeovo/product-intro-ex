from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

class PostHistory:
    """投稿履歴モデル"""
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    platform = Column(String(50), nullable=False)  # 'note' or 'twitter'
    post_content = Column(Text)
    posted_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='success')  # 'success' or 'failed'
    error_message = Column(Text)
