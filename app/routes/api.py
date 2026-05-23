from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.models import db, Product, PostHistory
from app.utils.metadata_extractor import extract_metadata
from app.services.claude_service import ClaudeService
import logging
import requests
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'url': p.url,
        'title': p.title,
        'description': p.description,
        'image_url': p.image_url,
        'category': p.category,
        'created_at': p.created_at.isoformat()
    } for p in products]), 200

@api.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        metadata = extract_metadata(url)

        product = Product(
            url=url,
            title=metadata.get('title', 'No title'),
            description=metadata.get('description'),
            image_url=metadata.get('image_url'),
            category=metadata.get('category', 'uncategorized')
        )

        db.session.add(product)
        db.session.commit()

        return jsonify({
            'id': product.id,
            'url': product.url,
            'title': product.title,
            'image_url': product.image_url
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Product URL already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    return jsonify({
        'id': product.id,
        'url': product.url,
        'title': product.title,
        'description': product.description,
        'image_url': product.image_url,
        'category': product.category,
        'created_at': product.created_at.isoformat()
    }), 200

@api.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200

@api.route('/history', methods=['GET'])
def get_history():
    history = PostHistory.query.order_by(PostHistory.posted_at.desc()).all()
    return jsonify([{
        'id': h.id,
        'product_id': h.product_id,
        'platform': h.platform,
        'posted_at': h.posted_at.isoformat(),
        'status': h.status
    } for h in history]), 200

@api.route('/products/<int:product_id>/generate-intro', methods=['POST'])
def generate_product_intro_api(product_id):
    """商品の紹介文を生成（Note用 + Twitter用）"""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    try:
        # Claude で紹介文を生成
        claude_service = ClaudeService()

        note_intro = claude_service.generate_product_intro(
            product.title,
            product.description or "",
            product.image_url
        )

        twitter_intro = claude_service.generate_twitter_intro(
            product.title,
            product.description or ""
        )

        if not note_intro or not twitter_intro:
            logger.error(f"Failed to generate intros for product {product_id}")
            return jsonify({'error': 'Failed to generate intros'}), 500

        affiliate_url = product.affiliate_url or product.url

        return jsonify({
            'success': True,
            'product_id': product_id,
            'note_intro': note_intro,
            'twitter_intro': twitter_intro,
            'affiliate_url': affiliate_url
        }), 200

    except Exception as e:
        logger.error(f"Error generating intros: {e}")
        return jsonify({'error': str(e)}), 500
