import requests
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class RakutenService:
    """楽天商品検索 API からアフィリエイト商品を取得するサービス"""

    def __init__(self):
        self.api_key = os.getenv('RAKUTEN_API_KEY')
        self.affiliate_id = os.getenv('RAKUTEN_AFFILIATE_ID', '')
        self.base_url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"

        if not self.api_key:
            logger.warning("RAKUTEN_API_KEY is not set. Rakuten API will not work.")

    def search_products(self, keyword=None, limit=3):
        """
        楽天商品検索 API で商品を検索

        Args:
            keyword (str): 検索キーワード
            limit (int): 取得件数

        Returns:
            list: 商品情報のリスト
                例: [
                    {
                        'itemUrl': 'https://...',
                        'itemName': '商品名',
                        'itemCaption': '説明',
                        'mediumImageUrl': '画像URL',
                        'affiliateUrl': 'アフィリエイトURL',
                        'genreId': 'ジャンルID'
                    },
                    ...
                ]

        Raises:
            Exception: API 呼び出し失敗時
        """
        if not self.api_key:
            logger.error("RAKUTEN_API_KEY is not set")
            return []

        if not keyword:
            keyword = os.getenv('RAKUTEN_SEARCH_KEYWORD', '便利グッズ')

        try:
            params = {
                'applicationId': self.api_key,
                'keyword': keyword,
                'hits': limit,
                'sort': '-salesDate',  # 新しい順
                'formatVersion': 2
            }

            logger.info(f"Rakuten API: searching for '{keyword}' (limit={limit})")
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if 'Items' not in data or not data['Items']:
                logger.warning(f"No products found for keyword: {keyword}")
                return []

            products = []
            for item in data['Items']:
                product_info = self._parse_item(item.get('Item', {}))
                if product_info:
                    products.append(product_info)

            logger.info(f"Rakuten API: Found {len(products)} products")
            return products

        except requests.exceptions.Timeout:
            logger.error("Rakuten API: Request timeout")
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f"Rakuten API request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"Error parsing Rakuten response: {e}")
            return []

    def _parse_item(self, item):
        """
        楽天 API のアイテムオブジェクトを ParsedProduct に変換

        Args:
            item (dict): 楽天 API から取得したアイテム

        Returns:
            dict: パースされた商品情報、またはパース失敗時は None
        """
        try:
            # 必須フィールドの確認
            if 'itemUrl' not in item or 'itemName' not in item:
                return None

            item_url = item.get('itemUrl', '')
            affiliate_url = item_url

            # アフィリエイト ID がある場合、URL に付与
            if self.affiliate_id:
                affiliate_url = self._build_affiliate_url(item_url)

            return {
                'itemUrl': item_url,
                'itemName': item.get('itemName', 'Unknown'),
                'itemCaption': item.get('itemCaption', ''),
                'mediumImageUrl': item.get('mediumImageUrl', ''),
                'affiliateUrl': affiliate_url,
                'genreId': item.get('genreId', 'uncategorized')
            }

        except Exception as e:
            logger.error(f"Error parsing Rakuten item: {e}")
            return None

    def _build_affiliate_url(self, item_url):
        """
        楽天アフィリエイト ID を URL に付与

        Args:
            item_url (str): 元の商品 URL

        Returns:
            str: アフィリエイト付きの URL
        """
        if not self.affiliate_id or not item_url:
            return item_url

        try:
            # URL に afid パラメータを追加
            separator = '&' if '?' in item_url else '?'
            return f"{item_url}{separator}afid={self.affiliate_id}"
        except Exception as e:
            logger.error(f"Error building affiliate URL: {e}")
            return item_url
