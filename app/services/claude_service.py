import anthropic
import os
import logging

logger = logging.getLogger(__name__)

class ClaudeService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))

    def generate_product_intro(self, product_title, product_description, image_url=None):
        """商品紹介文を生成"""
        prompt = f"""
商品を魅力的に紹介するSNS投稿文を生成してください。

商品名: {product_title}
説明: {product_description}
画像URL: {image_url}

要件：
- 清潔感があり、物珍しさを感じさせるトーン（トバログ・ミヤマレベッカ風）
- Note投稿向けの詳細な説明版（300-400字）を生成
- 絵文字は適度に使用
- 購買欲を刺激する表現
- 実際のメリット・特徴を盛り込む

投稿文：
"""
        try:
            message = self.client.messages.create(
                model="claude-opus-4-7",
                max_tokens=500,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return message.content[0].text.strip()
        except Exception as e:
            logger.error(f"Error generating intro: {e}")
            return None

    def generate_twitter_intro(self, product_title, product_description):
        """Twitter投稿用の短い紹介文を生成"""
        prompt = f"""
Twitter/X投稿用（280字以内）の商品紹介文を生成してください。

商品名: {product_title}
説明: {product_description}

要件：
- 280字以内
- 簡潔で印象的
- ハッシュタグ1-2個を含む
- 購買リンク付記のコンテキスト想定

投稿文：
"""
        try:
            message = self.client.messages.create(
                model="claude-opus-4-7",
                max_tokens=100,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return message.content[0].text.strip()
        except Exception as e:
            logger.error(f"Error generating twitter intro: {e}")
            return None
