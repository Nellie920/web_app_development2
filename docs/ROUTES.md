# ROUTES - 食譜收藏夾 路由與頁面設計

這份文件基於 PRD、架構圖與資料庫設計，規劃專案所有的 URL 路由、HTTP 方法以及對應的 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 (食譜列表) | `GET` | `/` | `templates/index.html` | 顯示所有食譜縮圖與基本資訊 |
| 查看食譜詳細 | `GET` | `/recipe/<int:id>` | `templates/detail.html` | 顯示特定食譜的完整材料、步驟與留言 |
| 新增食譜頁面 | `GET` | `/recipe/new` | `templates/edit.html` | 顯示新增食譜表單 |
| 送出新增食譜 | `POST` | `/recipe/new` | — | 接收表單，存入資料庫，重導向首頁 |
| 編輯食譜頁面 | `GET` | `/recipe/<int:id>/edit` | `templates/edit.html` | 顯示編輯食譜表單（共用） |
| 送出編輯食譜 | `POST` | `/recipe/<int:id>/edit` | — | 更新資料庫該筆資料，重導向詳細頁 |
| 刪除食譜 | `POST` | `/recipe/<int:id>/delete`| — | 刪除資料庫中的特定食譜，重導向首頁 |
| 新增留言 | `POST` | `/recipe/<int:id>/comment`| — | 接收留言並存入 DB，重導向詳細頁 |
| 按讚食譜 | `POST` | `/recipe/<int:id>/like` | — | 更新 Recipe 按讚數，回傳 JSON 或重導向 |

---

## 2. 每個路由的詳細說明

### 2.1 首頁 (食譜列表)
- **路徑與方法**：`GET /` (可加別名 `GET /recipes`)
- **輸入**：無
- **處理邏輯**：透過 Model 查詢所有 Recipe，依照建立時間反向排序 (最新在前)。
- **輸出**：渲染 `index.html`，傳入 `recipes` 陣列給前端。
- **錯誤處理**：資料庫為空時，前台顯示「目前尚無食譜，來新增第一道菜吧！」等提示。

### 2.2 查看食譜詳細
- **路徑與方法**：`GET /recipe/<int:id>`
- **輸入**：URL 路徑參數 `id`
- **處理邏輯**：透過 Model 查詢對應 `id` 的 Recipe，以及其所有的 Comment。
- **輸出**：渲染 `detail.html`，傳入 `recipe` 與 `comments` 給前端。
- **錯誤處理**：若該 `id` 不存在，回傳 404 狀態碼並顯示錯誤頁面。

### 2.3 新增食譜頁面
- **路徑與方法**：`GET /recipe/new`
- **輸入**：無
- **處理邏輯**：準備空白表單狀態供使用者填寫。
- **輸出**：渲染 `edit.html`。

### 2.4 送出新增食譜
- **路徑與方法**：`POST /recipe/new`
- **輸入**：表單資料 (`title`, `materials`, `steps`) 以及上傳圖片 (`image`)
- **處理邏輯**：
  1. 驗證必填欄位 (標題、材料、步驟)。
  2. 若有上傳圖片，驗證副檔名，並存入 `static/uploads/`，取得相對路徑。
  3. 呼叫 Model 建立新的 Recipe 紀錄並存入資料庫。
- **輸出**：重導向 (`redirect`) 回首頁 `/`。
- **錯誤處理**：若驗證失敗，回傳提示訊息並重新渲染 `edit.html` 讓使用者修正。

### 2.5 編輯食譜頁面
- **路徑與方法**：`GET /recipe/<int:id>/edit`
- **輸入**：URL 路徑參數 `id`
- **處理邏輯**：透過 Model 查詢對應 `id` 的 Recipe 物件。
- **輸出**：渲染 `edit.html`，傳入 `recipe` 物件，供表單填入預設值。
- **錯誤處理**：若 `id` 不存在，回傳 404。

### 2.6 送出編輯食譜
- **路徑與方法**：`POST /recipe/<int:id>/edit`
- **輸入**：URL 路徑參數 `id`，表單資料 (`title`, `materials`, `steps`)，以及可選的更新圖片 (`image`)
- **處理邏輯**：
  1. 查詢出原本的 Recipe 物件。
  2. 更新其文字欄位屬性。
  3. 若有上傳新圖片，將新圖片存入資料夾並更新 `image_path`，可選擇刪除舊圖片檔案。
  4. 儲存變更到資料庫。
- **輸出**：重導向至詳細頁 `/recipe/<id>`。

### 2.7 刪除食譜
- **路徑與方法**：`POST /recipe/<int:id>/delete`
- **輸入**：URL 路徑參數 `id`
- **處理邏輯**：
  1. 查詢出原本的 Recipe 物件。
  2. 刪除資料庫中的 Recipe 與關聯的 Comment。
  3. (可選) 刪除系統中該食譜的圖片檔案。
- **輸出**：重導向至首頁 `/`。

### 2.8 新增留言
- **路徑與方法**：`POST /recipe/<int:id>/comment`
- **輸入**：URL 路徑參數 `id`，表單資料 (`content`)
- **處理邏輯**：建立新的 Comment 物件，關聯到 `recipe_id`，存入資料庫。
- **輸出**：重導向至詳細頁 `/recipe/<id>`。

### 2.9 按讚食譜
- **路徑與方法**：`POST /recipe/<int:id>/like`
- **輸入**：URL 路徑參數 `id`
- **處理邏輯**：找到對應 Recipe 物件，將 `likes` 欄位 +1。
- **輸出**：回傳 JSON `{"likes": <新數量>}`，供前端使用 Vanilla JS AJAX 非同步更新。

---

## 3. Jinja2 模板清單

所有模板皆存放在 `app/templates/` 目錄。

1. **`base.html`**
   - **功能**：全局基礎版型，包含 HTML 結構、引用的 CSS/JS 資源、網站 Header (導航列) 與 Footer。
   - **繼承**：無，為其他檔案的基礎。

2. **`index.html`**
   - **功能**：首頁，顯示全部食譜卡片 (縮圖、標題、建立日期、讚數)。
   - **繼承**：`{% extends "base.html" %}`

3. **`detail.html`**
   - **功能**：食譜詳細頁，顯示大圖、完整材料清單、步驟、留言板、按讚按鈕與編輯/刪除按鈕。
   - **繼承**：`{% extends "base.html" %}`

4. **`edit.html`**
   - **功能**：新增與編輯食譜共用之表單頁面。若傳入 `recipe` 物件則帶出舊資料為「編輯」，否則為「新增」。
   - **繼承**：`{% extends "base.html" %}`
