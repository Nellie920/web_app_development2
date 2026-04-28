# ROUTES - 食譜收藏夾 路由設計與頁面規劃

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **食譜列表 (首頁)** | GET | `/` | `templates/index.html` | 顯示所有食譜縮圖與基本資訊 |
| **新增食譜頁面** | GET | `/recipe/new` | `templates/recipe_form.html` | 顯示新增食譜表單 |
| **建立食譜** | POST | `/recipe/new` | — | 接收表單資料、儲存圖片，寫入 DB 後重導向至首頁 |
| **食譜詳細頁** | GET | `/recipe/<int:id>` | `templates/recipe_detail.html`| 顯示單篇食譜完整資訊與留言 |
| **編輯食譜頁面** | GET | `/recipe/<int:id>/edit`| `templates/recipe_form.html` | 顯示編輯表單，並帶入原本資料 |
| **更新食譜** | POST | `/recipe/<int:id>/update`| — | 接收更新表單資料，更新 DB 後重導向至詳細頁 |
| **刪除食譜** | POST | `/recipe/<int:id>/delete`| — | 刪除資料與圖片，重導向至首頁 |
| **新增留言** | POST | `/recipe/<int:id>/comment`| — | 接收留言內容，寫入 DB 後重導向至詳細頁 |
| **按讚食譜** | POST | `/recipe/<int:id>/like`| — | 更新按讚數，回傳 JSON (供前端 AJAX 使用) |

---

## 2. 每個路由的詳細說明

### 1. `GET /` (食譜列表)
- **輸入**：無
- **處理邏輯**：查詢 `Recipe` 表格中所有資料，按建立時間反向排序。
- **輸出**：渲染 `index.html`，傳遞 `recipes` 變數。
- **錯誤處理**：無。

### 2. `GET /recipe/new` (新增食譜頁面)
- **輸入**：無
- **處理邏輯**：無特殊邏輯。
- **輸出**：渲染 `recipe_form.html`，可傳遞 `action="create"` 等變數供模板判斷。

### 3. `POST /recipe/new` (建立食譜)
- **輸入**：表單欄位 (`title`, `materials`, `steps`, `image` 檔案)
- **處理邏輯**：
  1. 驗證必填欄位。
  2. 若有圖片，將圖片儲存至 `static/uploads/` 並取得路徑。
  3. 建立 `Recipe` 物件並存入資料庫。
- **輸出**：重導向 `redirect(url_for('index'))`。
- **錯誤處理**：驗證失敗則重新渲染 `recipe_form.html` 並顯示錯誤訊息。

### 4. `GET /recipe/<id>` (食譜詳細頁)
- **輸入**：URL 參數 `id`
- **處理邏輯**：查詢該 `id` 的 `Recipe` 資料，以及關聯的所有 `Comment` 資料。
- **輸出**：渲染 `recipe_detail.html`，傳遞 `recipe` 與 `comments` 變數。
- **錯誤處理**：若 `id` 不存在，回傳 404 頁面或重導向首頁並提示。

### 5. `GET /recipe/<id>/edit` (編輯食譜頁面)
- **輸入**：URL 參數 `id`
- **處理邏輯**：查詢該 `id` 的 `Recipe` 資料。
- **輸出**：渲染 `recipe_form.html`，將查出的資料填入表單預設值。
- **錯誤處理**：若 `id` 不存在，回傳 404 頁面。

### 6. `POST /recipe/<id>/update` (更新食譜)
- **輸入**：URL 參數 `id`，表單欄位
- **處理邏輯**：
  1. 查詢該 `id` 的 `Recipe` 資料。
  2. 驗證並更新欄位。若有新圖片，取代舊圖片檔案。
  3. 儲存變更至資料庫。
- **輸出**：重導向 `redirect(url_for('recipe_detail', id=id))`。
- **錯誤處理**：驗證失敗則重導向或重新渲染表單。

### 7. `POST /recipe/<id>/delete` (刪除食譜)
- **輸入**：URL 參數 `id`
- **處理邏輯**：查詢並刪除該 `id` 的 `Recipe`，並刪除對應的實體圖片檔案。
- **輸出**：重導向 `redirect(url_for('index'))`。

### 8. `POST /recipe/<id>/comment` (新增留言)
- **輸入**：URL 參數 `id`，表單欄位 `content`
- **處理邏輯**：建立 `Comment` 物件並寫入資料庫。
- **輸出**：重導向 `redirect(url_for('recipe_detail', id=id))`。

### 9. `POST /recipe/<id>/like` (按讚食譜)
- **輸入**：URL 參數 `id`
- **處理邏輯**：將該 `Recipe` 的 `likes` 數量 +1。
- **輸出**：回傳 JSON `{"status": "success", "likes": new_likes_count}`。

---

## 3. Jinja2 模板清單

所有的模板將放置於 `app/templates/` 目錄。

1. **`base.html`**
   - **說明**：全站共用的版型（包含 HTML 骨架、`<head>` 的 CSS/JS 引入、可愛風格導覽列、頁尾）。
2. **`index.html`**
   - **說明**：首頁，繼承 `base.html`。顯示食譜清單（Card UI 設計）。
3. **`recipe_detail.html`**
   - **說明**：食譜詳細頁，繼承 `base.html`。顯示圖片、材料清單、製作步驟、留言區與按讚按鈕。
4. **`recipe_form.html`**
   - **說明**：新增/編輯共用表單頁，繼承 `base.html`。包含標題、材料、步驟與圖片上傳輸入框。
5. **`404.html`** (Nice to have)
   - **說明**：找不到頁面時的可愛風格錯誤提示。

---

## 4. 路由骨架程式碼
請參考 `app/routes/recipe_routes.py`。
