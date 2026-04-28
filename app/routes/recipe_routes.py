from flask import render_template, request, redirect, url_for, jsonify
from . import recipe_bp

@recipe_bp.route('/')
def index():
    """
    食譜列表 (首頁)
    查詢所有食譜並渲染 index.html
    """
    pass

@recipe_bp.route('/recipe/new', methods=['GET'])
def new_recipe():
    """
    新增食譜頁面
    渲染 recipe_form.html
    """
    pass

@recipe_bp.route('/recipe/new', methods=['POST'])
def create_recipe():
    """
    建立食譜
    接收表單資料，儲存圖片，存入資料庫後重導向至首頁
    """
    pass

@recipe_bp.route('/recipe/<int:id>')
def recipe_detail(id):
    """
    食譜詳細頁
    根據 id 查詢單筆食譜與關聯留言，渲染 recipe_detail.html
    """
    pass

@recipe_bp.route('/recipe/<int:id>/edit', methods=['GET'])
def edit_recipe(id):
    """
    編輯食譜頁面
    根據 id 查詢食譜資料，渲染 recipe_form.html 並帶入預設值
    """
    pass

@recipe_bp.route('/recipe/<int:id>/update', methods=['POST'])
def update_recipe(id):
    """
    更新食譜
    接收表單資料更新資料庫，完成後重導向至詳細頁
    """
    pass

@recipe_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除食譜
    刪除特定食譜與關聯圖片，完成後重導向至首頁
    """
    pass

@recipe_bp.route('/recipe/<int:id>/comment', methods=['POST'])
def add_comment(id):
    """
    新增留言
    接收留言內容存入資料庫，重導向至詳細頁
    """
    pass

@recipe_bp.route('/recipe/<int:id>/like', methods=['POST'])
def like_recipe(id):
    """
    按讚食譜
    將食譜的讚數加 1，回傳 JSON 格式的最新讚數
    """
    pass
