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
from app.services.rakuten_service import RakutenService

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()

class ProductScheduler:
    def __init__(self):
        self.claude_service = ClaudeService()
        self.sns_service = SNSService()
        self.rakuten_service = RakutenService()
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

    def auto_fetch_rakuten_products(self):
        """毎日 00:00 JST に楽天から新商品を自動取得（3 件）"""
        try:
            keyword = os.getenv('RAKUTEN_SEARCH_KEYWORD', '便利グッズ')
            limit = int(os.getenv('RAKUTEN_FETCH_LIMIT', 3))

            items = self.rakuten_service.search_products(keyword, limit)

            if not items:
                logger.warning("No products fetched from Rakuten")
                return

            added_count = 0
            for item in items:
                try:
                    # 重複チェック
                    existing = Product.query.filter_by(url=item['itemUrl']).first()
                    if existing:
                        logger.info(f"Product already exists: {item['itemUrl']}")
                        continue

                    # 新規商品作成
                    product = Product(
                        url=item['itemUrl'],
                        title=item['itemName'],
                        description=item.get('itemCaption', ''),
                        image_url=item.get('mediumImageUrl', ''),
                        category='rakuten',
                        is_affiliate=True,
                        affiliate_url=item.get('affiliateUrl', item['itemUrl'])
                    )

                    db.session.add(product)
                    added_count += 1

                except Exception as e:
                    logger.error(f"Failed to add Rakuten product: {e}")
                    continue

            db.session.commit()
            logger.info(f"Rakuten auto-fetch: {added_count} products added")

        except Exception as e:
            logger.error(f"Rakuten auto-fetch failed: {e}")
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

        # 楽天自動取得：毎日 00:00 JST
        scheduler.add_job(
            product_scheduler.auto_fetch_rakuten_products,
            trigger=CronTrigger(hour=0, minute=0, day_of_week='mon-sun'),
            id='rakuten_auto_fetch',
            name='Rakuten auto-fetch'
        )

        scheduler.start()
        logger.info(f"Scheduler started. Daily post at {post_time} JST")

def stop_scheduler():
    """スケジューラー停止"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")
