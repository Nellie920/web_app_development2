import os
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, current_app
from werkzeug.utils import secure_filename
from app.models.recipe import Recipe, Comment

recipe_bp = Blueprint('recipe', __name__)

# 設定允許上傳的圖片副檔名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@recipe_bp.route('/')
@recipe_bp.route('/recipes')
def index():
    """首頁 (食譜列表)"""
    recipes = Recipe.get_all()
    return render_template('index.html', recipes=recipes)

@recipe_bp.route('/recipe/<int:id>')
def detail(id):
    """查看食譜詳細"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜', 'error')
        return redirect(url_for('recipe.index'))
    return render_template('detail.html', recipe=recipe, comments=recipe.comments)

@recipe_bp.route('/recipe/new', methods=['GET', 'POST'])
def create_recipe():
    """新增食譜"""
    if request.method == 'POST':
        title = request.form.get('title')
        materials = request.form.get('materials')
        steps = request.form.get('steps')
        
        if not title or not materials or not steps:
            flash('標題、材料與步驟皆為必填欄位！', 'error')
            return redirect(url_for('recipe.create_recipe'))

        # 處理圖片上傳
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                file_path = os.path.join(upload_dir, filename)
                file.save(file_path)
                image_path = f'uploads/{filename}'
        
        data = {
            'title': title,
            'materials': materials,
            'steps': steps,
            'image_path': image_path
        }
        
        try:
            Recipe.create(data)
            flash('食譜新增成功！', 'success')
            return redirect(url_for('recipe.index'))
        except Exception as e:
            flash(f'發生錯誤：{str(e)}', 'error')
            
    return render_template('edit.html', recipe=None)

@recipe_bp.route('/recipe/<int:id>/edit', methods=['GET', 'POST'])
def edit_recipe(id):
    """編輯食譜"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜', 'error')
        return redirect(url_for('recipe.index'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        materials = request.form.get('materials')
        steps = request.form.get('steps')
        
        if not title or not materials or not steps:
            flash('標題、材料與步驟皆為必填欄位！', 'error')
            return redirect(url_for('recipe.edit_recipe', id=id))
            
        data = {
            'title': title,
            'materials': materials,
            'steps': steps
        }
        
        # 處理圖片上傳
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                file_path = os.path.join(upload_dir, filename)
                file.save(file_path)
                data['image_path'] = f'uploads/{filename}'
        
        try:
            recipe.update(data)
            flash('食譜更新成功！', 'success')
            return redirect(url_for('recipe.detail', id=id))
        except Exception as e:
            flash(f'發生錯誤：{str(e)}', 'error')
            
    return render_template('edit.html', recipe=recipe)

@recipe_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """刪除食譜"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜', 'error')
        return redirect(url_for('recipe.index'))
        
    try:
        recipe.delete()
        flash('食譜已成功刪除！', 'success')
    except Exception as e:
        flash(f'發生錯誤：{str(e)}', 'error')
        
    return redirect(url_for('recipe.index'))

@recipe_bp.route('/recipe/<int:id>/comment', methods=['POST'])
def add_comment(id):
    """新增留言"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜', 'error')
        return redirect(url_for('recipe.index'))
        
    content = request.form.get('content')
    if not content:
        flash('留言內容不可為空！', 'error')
        return redirect(url_for('recipe.detail', id=id))
        
    data = {
        'recipe_id': id,
        'content': content
    }
    
    try:
        Comment.create(data)
        flash('留言成功！', 'success')
    except Exception as e:
        flash(f'發生錯誤：{str(e)}', 'error')
        
    return redirect(url_for('recipe.detail', id=id))

@recipe_bp.route('/recipe/<int:id>/like', methods=['POST'])
def like_recipe(id):
    """按讚食譜"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404
        
    try:
        recipe.update({'likes': recipe.likes + 1})
        return jsonify({'likes': recipe.likes})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
