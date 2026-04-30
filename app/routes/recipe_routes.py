from flask import Blueprint, render_template, request, redirect, url_for, jsonify

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
@recipe_bp.route('/recipes')
def index():
    """
    首頁 (食譜列表)
    - 輸入：無
    - 處理邏輯：查詢所有 Recipe，依照建立時間反向排序
    - 輸出：渲染 index.html，傳入 recipes 變數
    """
    pass

@recipe_bp.route('/recipe/<int:id>')
def detail(id):
    """
    查看食譜詳細
    - 輸入：URL 參數 id
    - 處理邏輯：以 ID 查詢 Recipe 以及關聯的 Comment
    - 輸出：渲染 detail.html，傳入 recipe 與 comments 變數
    """
    pass

@recipe_bp.route('/recipe/new', methods=['GET', 'POST'])
def create_recipe():
    """
    新增食譜
    - 輸入：GET(無), POST(表單 title, materials, steps, 圖片 image)
    - 處理邏輯：
        - GET: 準備空表單狀態
        - POST: 驗證必填，儲存圖片，建立 Recipe 寫入 DB
    - 輸出：GET 渲染 edit.html，POST 重導向至首頁
    """
    pass

@recipe_bp.route('/recipe/<int:id>/edit', methods=['GET', 'POST'])
def edit_recipe(id):
    """
    編輯食譜
    - 輸入：GET(URL 參數 id), POST(URL 參數 id, 表單資料與可選圖片)
    - 處理邏輯：
        - GET: 查詢 Recipe，填入表單初始值
        - POST: 更新 Recipe 屬性，若有新圖片則替換並儲存至 DB
    - 輸出：GET 渲染 edit.html，POST 重導向至詳細頁
    """
    pass

@recipe_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除食譜
    - 輸入：URL 參數 id
    - 處理邏輯：查詢 Recipe，刪除相關 Comment 與 Recipe 及本地圖片
    - 輸出：重導向至首頁
    """
    pass

@recipe_bp.route('/recipe/<int:id>/comment', methods=['POST'])
def add_comment(id):
    """
    新增留言
    - 輸入：URL 參數 id, 表單 content
    - 處理邏輯：建立 Comment 關聯 recipe_id，存入 DB
    - 輸出：重導向至詳細頁
    """
    pass

@recipe_bp.route('/recipe/<int:id>/like', methods=['POST'])
def like_recipe(id):
    """
    按讚食譜
    - 輸入：URL 參數 id
    - 處理邏輯：找到 Recipe，將 likes 欄位加一
    - 輸出：回傳 JSON {"likes": 新數量}
    """
    pass
