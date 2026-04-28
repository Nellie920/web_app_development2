# ARCHITECTURE - 食譜收藏夾 系統架構設計

## 1. 技術架構說明
- **選用技術與原因**：
  - **後端：Python + Flask**。Flask 是一個輕量級的網頁框架，適合用來快速開發小型至中型的應用程式，學習曲線平緩，且能靈活搭配不同的套件。
  - **模板引擎：Jinja2**。內建於 Flask 中，可以直接將後端資料注入 HTML，無需另外處理複雜的 API 與前端狀態管理，適合不需前後端分離的專案。
  - **資料庫：SQLite + SQLAlchemy (ORM)**。SQLite 不需要額外架設資料庫伺服器，資料會直接儲存在單一檔案中，非常適合初期專案與個人使用。搭配 SQLAlchemy 可以用 Python 語法操作資料庫，避免撰寫繁瑣的 SQL 語句。
  - **前端：HTML/CSS/JavaScript (Vanilla)**。為了實現「可愛圓潤」的風格，我們將自行撰寫 CSS，或套用輕量級且易於客製化風格的 CSS 框架，不採用過於龐大的前端框架，保持專案輕量。

- **Flask MVC 模式說明**：
  - **Model (模型)**：負責定義資料結構（例如「食譜」包含哪些欄位），並處理與 SQLite 資料庫的溝通（新增、查詢、修改、刪除）。
  - **View (視圖)**：負責呈現給使用者的畫面。在我們的專案中，就是寫好的 Jinja2 HTML 模板，會接收 Controller 傳來的資料並渲染出來。
  - **Controller (控制器)**：由 Flask 的路由（Routes）負責。它會接收來自使用者瀏覽器的請求（例如：點擊「儲存食譜」），去呼叫對應的 Model 處理資料，最後把結果交給 View 去產生 HTML 畫面回傳給瀏覽器。

## 2. 專案資料夾結構

```text
app/
├── __init__.py         # 應用程式工廠，初始化 Flask app 與套件
├── models/             # 資料庫模型 (Model)
│   ├── __init__.py
│   └── recipe.py       # 定義食譜、評論等資料表結構
├── routes/             # Flask 路由 (Controller)
│   ├── __init__.py
│   └── recipe_routes.py # 處理食譜相關的請求
├── templates/          # Jinja2 HTML 模板 (View)
│   ├── base.html       # 共用版型（包含導覽列、頁尾）
│   ├── index.html      # 首頁（食譜列表）
│   ├── detail.html     # 食譜詳細頁
│   └── edit.html       # 新增/編輯食譜頁面
└── static/             # CSS / JS / 圖片等靜態資源
    ├── css/
    │   └── style.css   # 可愛圓潤風格的自訂樣式表
    ├── js/
    │   └── main.js     # 負責前端互動（如按讚的非同步處理）
    └── uploads/        # 儲存使用者上傳的食譜圖片
instance/
└── database.db         # SQLite 資料庫檔案
app.py                  # 專案執行入口檔案
requirements.txt        # Python 依賴套件清單
docs/                   # 專案設計文件 (PRD, 架構圖等)
```

## 3. 元件關係圖

```mermaid
graph LR
    User[瀏覽器 / 使用者] -- HTTP Request --> Routes[Flask Route (Controller)]
    Routes -- 讀寫資料 --> Models[Model (SQLAlchemy)]
    Models -- 執行 SQL --> DB[(SQLite Database)]
    DB -- 傳回資料 --> Models
    Models -- 傳回物件 --> Routes
    Routes -- 傳遞資料 --> Templates[Jinja2 Template (View)]
    Templates -- 渲染 HTML --> Routes
    Routes -- HTTP Response (HTML) --> User
```

## 4. 關鍵設計決策
1. **採用 Monolith (單體式) 架構而非前後端分離**：
   - *原因*：對於像「食譜收藏夾」這類以展示資訊為主、互動單純的應用，使用 Flask + Jinja2 直接渲染頁面，可以省去開發與維護 API 的時間，讓開發重心放在功能實作與畫面設計上。
2. **圖片儲存於本機檔案系統 (`static/uploads`)**：
   - *原因*：初期 MVP 階段不引入雲端儲存服務（如 AWS S3），降低部署門檻與複雜度。會在資料庫中僅儲存圖片的「相對路徑檔名」。
3. **自訂 Vanilla CSS 實作可愛風格**：
   - *原因*：主流 CSS 框架（如 Bootstrap）預設風格較偏商務或科技感，要完全覆蓋成「可愛圓潤」風格反而費時。直接撰寫 CSS 或使用變數設定 `border-radius: 20px`, 柔和色系 (`#FFB6C1` 等) 與圓潤字體，能更精準達到設計要求。
   - *實作細節*：預計會建立全局的 CSS 變數（CSS Variables）來統一管理色系與字體，方便未來快速切換或微調風格。
