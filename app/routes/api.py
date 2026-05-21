from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.main import db
from app.models import Product, PostHistory
from app.utils.metadata_extractor import extract_metadata
import requests
from PIL import Image
from io import BytesIO

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
