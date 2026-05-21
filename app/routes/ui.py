from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import db, Product, PostHistory
from sqlalchemy import func
from datetime import datetime, timedelta

ui = Blueprint('ui', __name__, url_prefix='/')

@ui.route('/', methods=['GET'])
def dashboard():
    """メインダッシュボード"""
    total_products = db.session.query(func.count(Product.id)).scalar() or 0
    total_posts = db.session.query(func.count(PostHistory.id)).scalar() or 0

    recent_posts = PostHistory.query.order_by(PostHistory.posted_at.desc()).limit(10).all()

    last_7_days = datetime.utcnow() - timedelta(days=7)
    posts_last_week = db.session.query(func.count(PostHistory.id)).filter(
        PostHistory.posted_at >= last_7_days
    ).scalar() or 0

    return render_template('dashboard.html',
                         total_products=total_products,
                         total_posts=total_posts,
                         recent_posts=recent_posts,
                         posts_last_week=posts_last_week)

@ui.route('/products', methods=['GET'])
def products_list():
    """商品一覧"""
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=20)
    return render_template('products.html', products=products)

@ui.route('/products/add', methods=['GET', 'POST'])
def add_product():
    """商品追加フォーム"""
    if request.method == 'POST':
        url = request.form.get('url')
        title = request.form.get('title')
        description = request.form.get('description')

        if not url or not title:
            flash('URL and Title are required', 'error')
            return redirect(url_for('ui.add_product'))

        try:
            product = Product(
                url=url,
                title=title,
                description=description,
                category=request.form.get('category', 'uncategorized')
            )
            db.session.add(product)
            db.session.commit()
            flash(f'Product "{title}" added successfully!', 'success')
            return redirect(url_for('ui.products_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')

    return render_template('add_product.html')

@ui.route('/products/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    """商品削除"""
    product = Product.query.get(product_id)
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('ui.products_list'))

    try:
        db.session.delete(product)
        db.session.commit()
        flash(f'Product "{product.title}" deleted', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')

    return redirect(url_for('ui.products_list'))

@ui.route('/history', methods=['GET'])
def post_history():
    """投稿履歴"""
    page = request.args.get('page', 1, type=int)
    history = PostHistory.query.order_by(PostHistory.posted_at.desc()).paginate(page=page, per_page=20)
    return render_template('history.html', history=history)
