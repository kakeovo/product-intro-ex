import requests
import os
import logging
import json

logger = logging.getLogger(__name__)

class SNSService:
    def __init__(self):
        self.note_api_key = os.getenv('NOTE_API_KEY')
        self.twitter_bearer = os.getenv('TWITTER_API_KEY')

    def post_to_note(self, product, content):
        """Note にテキスト投稿"""
        if not self.note_api_key:
            logger.warning("Note API key not configured")
            return False

        try:
            url = "https://api.note.com/v1/posts"
            headers = {
                'Authorization': f'Bearer {self.note_api_key}',
                'Content-Type': 'application/json'
            }

            payload = {
                'title': f"【紹介】{product.title}",
                'body': content,
                'source_url': product.url,
                'publish': True
            }

            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code in [200, 201]:
                logger.info(f"Posted to Note: {product.title}")
                return True
            else:
                logger.error(f"Note post failed: {response.text}")
                return False

        except Exception as e:
            logger.error(f"Error posting to Note: {e}")
            return False

    def post_to_twitter(self, product, content):
        """Twitter にツイート投稿"""
        if not self.twitter_bearer:
            logger.warning("Twitter API not configured")
            return False

        try:
            url = "https://api.twitter.com/2/tweets"
            headers = {
                'Authorization': f'Bearer {self.twitter_bearer}',
                'Content-Type': 'application/json'
            }

            full_content = f"{content}\n\n{product.url}"
            payload = {
                'text': full_content
            }

            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code in [200, 201]:
                logger.info(f"Posted to Twitter: {product.title}")
                return True
            else:
                logger.error(f"Twitter post failed: {response.text}")
                return False

        except Exception as e:
            logger.error(f"Error posting to Twitter: {e}")
            return False

    def post_with_image(self, product, content, platform='note'):
        """画像付き投稿"""
        if platform == 'note':
            return self._post_note_with_image(product, content)
        elif platform == 'twitter':
            return self._post_twitter_with_image(product, content)
        return False

    def _post_note_with_image(self, product, content):
        """Note に画像付き投稿（実装例）"""
        if not self.note_api_key or not product.image_url:
            return False

        try:
            image_response = requests.get(product.image_url, timeout=5)
            if image_response.status_code != 200:
                return False

            url = "https://api.note.com/v1/posts"
            headers = {
                'Authorization': f'Bearer {self.note_api_key}',
                'Content-Type': 'multipart/form-data'
            }

            files = {
                'image': ('product.jpg', image_response.content, 'image/jpeg')
            }

            data = {
                'title': f"【紹介】{product.title}",
                'body': content,
                'source_url': product.url,
                'publish': True
            }

            response = requests.post(url, files=files, data=data, headers=headers, timeout=10)
            return response.status_code in [200, 201]

        except Exception as e:
            logger.error(f"Error posting to Note with image: {e}")
            return False

    def _post_twitter_with_image(self, product, content):
        """Twitter に画像付きツイート（実装例）"""
        if not self.twitter_bearer or not product.image_url:
            return False

        try:
            image_response = requests.get(product.image_url, timeout=5)
            if image_response.status_code != 200:
                return False

            media_url = "https://upload.twitter.com/i/media/upload.json"
            headers = {
                'Authorization': f'Bearer {self.twitter_bearer}'
            }

            files = {
                'media_data': (None, image_response.content, 'image/jpeg')
            }

            media_response = requests.post(media_url, files=files, headers=headers, timeout=10)
            if media_response.status_code != 200:
                return False

            media_id = media_response.json()['media_id_string']

            tweet_url = "https://api.twitter.com/2/tweets"
            payload = {
                'text': f"{content}\n\n{product.url}",
                'media': {
                    'media_ids': [media_id]
                }
            }

            response = requests.post(tweet_url, json=payload, headers=headers, timeout=10)
            return response.status_code in [200, 201]

        except Exception as e:
            logger.error(f"Error posting to Twitter with image: {e}")
            return False
