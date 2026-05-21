from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
import logging
import random
from datetime import datetime
import os

from app.models import db, Product, PostHistory
from app.services.claude_service import ClaudeService
from app.services.sns_service import SNSService

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()

class ProductScheduler:
    def __init__(self):
        self.claude_service = ClaudeService()
        self.sns_service = SNSService()
        self.posted_product_ids = set()

    def select_random_product(self):
        """既出商品を除いて、ランダムに商品を選ぶ"""
        all_products = Product.query.all()
        available_products = [p for p in all_products if p.id not in self.posted_product_ids]

        if not available_products:
            logger.warning("No new products available, resetting history")
            self.posted_product_ids.clear()
            available_products = all_products

        return random.choice(available_products) if available_products else None

    def post_daily_product(self):
        """毎日自動で商品を投稿"""
        try:
            product = self.select_random_product()
            if not product:
                logger.warning("No products available to post")
                return

            note_intro = self.claude_service.generate_product_intro(
                product.title,
                product.description or "",
                product.image_url
            )

            twitter_intro = self.claude_service.generate_twitter_intro(
                product.title,
                product.description or ""
            )

            note_success = self.sns_service.post_to_note(product, note_intro)
            twitter_success = self.sns_service.post_to_twitter(product, twitter_intro)

            if note_success:
                history = PostHistory(
                    product_id=product.id,
                    platform='note',
                    post_content=note_intro,
                    status='success'
                )
                db.session.add(history)

            if twitter_success:
                history = PostHistory(
                    product_id=product.id,
                    platform='twitter',
                    post_content=twitter_intro,
                    status='success'
                )
                db.session.add(history)

            self.posted_product_ids.add(product.id)
            db.session.commit()
            logger.info(f"Posted product {product.id}: {product.title}")

        except Exception as e:
            logger.error(f"Error in daily post: {e}")
            db.session.rollback()

def start_scheduler():
    """バックグラウンド スケジューラー開始"""
    if not scheduler.running:
        scheduler.configure(
            executors={'default': ThreadPoolExecutor(max_workers=2)},
            job_defaults={'coalesce': False, 'max_instances': 1},
            timezone='Asia/Tokyo'
        )

        post_time = os.getenv('POST_TIME', '09:00')
        hour, minute = map(int, post_time.split(':'))

        product_scheduler = ProductScheduler()

        scheduler.add_job(
            product_scheduler.post_daily_product,
            trigger=CronTrigger(hour=hour, minute=minute, day_of_week='mon-sun'),
            id='daily_product_post',
            name='Daily product posting'
        )

        scheduler.start()
        logger.info(f"Scheduler started. Daily post at {post_time} JST")

def stop_scheduler():
    """スケジューラー停止"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")
