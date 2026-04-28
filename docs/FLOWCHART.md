# FLOWCHART - 食譜收藏夾 流程圖設計

以下為根據系統架構與需求所設計的流程圖，包含使用者操作路徑以及系統內部的資料流動序列。

## 1. 使用者流程圖（User Flow）

此流程圖描述使用者從進入網站開始，可以進行的各種操作路徑。

```mermaid
flowchart LR
    Start([使用者開啟網站]) --> Home[首頁 - 食譜列表]
    
    Home -->|點擊某篇食譜| Detail[食譜詳細頁]
    Detail -->|點擊按讚| Like[送出按讚]
    Like -.返回.-> Detail
    Detail -->|填寫留言| Comment[送出留言]
    Comment -.返回.-> Detail
    Detail -->|點擊分享| Share[複製網址]
    
    Home -->|點擊新增| Create[新增食譜頁面]
    Create -->|上傳圖片/填寫資料| SubmitCreate[送出新增]
    SubmitCreate -.成功.-> Home
    
    Detail -->|點擊編輯| Edit[編輯食譜頁面]
    Edit -->|修改資料| SubmitEdit[送出修改]
    SubmitEdit -.成功.-> Detail
    
    Detail -->|點擊刪除| Delete[確認刪除]
    Delete -.成功.-> Home
```

## 2. 系統序列圖（Sequence Diagram）

此序列圖描述當使用者「新增食譜」時，資料從瀏覽器傳遞到資料庫的完整流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route
    participant Model as SQLAlchemy Model
    participant DB as SQLite

    User->>Browser: 填寫表單（食譜名稱、圖片、材料、步驟）並點擊送出
    Browser->>Route: POST /recipe/new (含表單資料與檔案)
    
    rect rgb(240, 248, 255)
        Note over Route: 1. 驗證表單資料<br/>2. 儲存圖片至 static/uploads<br/>3. 取得圖片相對路徑
    end
    
    Route->>Model: 建立 Recipe 物件 (包含圖片路徑)
    Model->>DB: INSERT INTO recipe
    DB-->>Model: 回傳成功 (產生 id)
    Model-->>Route: Recipe 物件儲存成功
    Route-->>Browser: HTTP 302 重新導向至首頁 (GET /)
    Browser->>User: 顯示最新上傳的食譜列表
```

## 3. 功能清單與路由對照表

初步規劃的對應 URL 路徑與 HTTP 方法，以符合 RESTful 風格。

| 功能項目 | HTTP 方法 | URL 路徑 | 說明 |
| --- | --- | --- | --- |
| **瀏覽食譜列表** | `GET` | `/` 或 `/recipes` | 顯示所有食譜縮圖與基本資訊 |
| **查看食譜詳細** | `GET` | `/recipe/<id>` | 顯示特定食譜的完整材料、步驟與留言 |
| **新增食譜頁面** | `GET` | `/recipe/new` | 回傳新增食譜的 HTML 表單 |
| **送出新增食譜** | `POST` | `/recipe/new` | 接收表單資料，寫入資料庫並儲存圖片 |
| **編輯食譜頁面** | `GET` | `/recipe/<id>/edit` | 回傳帶有舊資料的編輯表單 |
| **送出編輯食譜** | `POST` | `/recipe/<id>/edit` | 更新資料庫中的該筆食譜資料 |
| **刪除食譜** | `POST` | `/recipe/<id>/delete`| 刪除資料庫中的特定食譜與相關留言 |
| **新增留言** | `POST` | `/recipe/<id>/comment`| 接收留言內容，寫入 Comment 資料表 |
| **按讚食譜** | `POST` | `/recipe/<id>/like` | 更新 Recipe 的按讚數 (可考慮用 AJAX) |
