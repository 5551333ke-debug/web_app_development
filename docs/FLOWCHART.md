# 系統流程圖 (FLOWCHART)

本文件使用 Mermaid 語法定義活動報名系統的操作流程與資料流向，幫助開發人員理解功能邏輯。

## 1. 使用者流程圖 (User Flow)

描述「參與者」與「主辦方」在系統中的主要操作路徑。

```mermaid
flowchart TD
    Start([開始]) --> Role{使用者身分?}
    
    %% 參與者流程
    Role -->|參與者| Home[首頁: 活動列表]
    Home --> Detail[活動詳情頁]
    Detail --> Register{點擊報名?}
    Register -->|是| Form[填寫報名表單]
    Form --> Submit[提交資料]
    Submit --> Success([報名成功頁 & 收到確認信])
    
    %% 主辦方流程
    Role -->|主辦方| Login[管理者登入]
    Login --> Dash[管理控制台]
    Dash --> Create[建立/編輯活動]
    Dash --> Manage[查看報名名單]
    Manage --> Export[匯出 CSV]
    Manage --> QR[現場 QR Code 簽到]
    
    Create --> Dash
    Export --> Dash
    QR --> Dash
```

---

## 2. 系統序列圖 (Sequence Diagram)

以「參與者提交報名表單」為例，展示系統內部元件的互動過程。

```mermaid
sequenceDiagram
    actor User as 參與者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as SQLAlchemy Model
    participant DB as SQLite DB
    participant Util as Utility (Email/QR)

    User->>Browser: 填寫姓名、Email、備註並點擊提交
    Browser->>Flask: POST /activity/id/register
    
    Note over Flask: 驗證欄位格式與剩餘名額
    
    Flask->>Model: 建立 Registration 實例
    Model->>DB: INSERT INTO registrations
    DB-->>Model: 成功儲存
    
    rect rgb(240, 240, 240)
        Note right of Util: 異步/背景處理 (模擬)
        Flask->>Util: 呼叫 qrcode_gen 產生票券
        Util-->>Flask: 回傳 QR Code 路徑/資料
        Flask->>Util: 呼叫 email_sender 寄送確認信
    end

    Flask-->>Browser: 重導向至 /success (攜帶票券資訊)
    Browser-->>User: 顯示「報名成功」與電子票券
```

---

## 3. 功能路徑對照表

以下為系統核心功能與對應的路由配置參考：

| 功能區域 | 功能名稱 | 建議 URL 路徑 | 方法 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **公開頁面** | 首頁 (活動列表) | `/` | GET | 展示所有進行中的活動 |
| | 活動詳情頁 | `/activity/<int:id>` | GET | 顯示活動說明、時間、剩餘名額 |
| | 提交報名 | `/activity/<int:id>/register` | POST | 接收報名資料並儲存 |
| | 報名成功頁 | `/registration/success` | GET | 顯示成功訊息與 QR Code |
| **管理後台** | 管理者登入 | `/admin/login` | GET/POST | 主辦身份驗證 |
| | 管理者控制台 | `/admin/dashboard` | GET | 活動清單管理與數據概覽 |
| | 建立活動 | `/admin/activity/new` | GET/POST | 設定活動標題、時間、報名規則 |
| | 名單管理 | `/admin/activity/<int:id>/list` | GET | 該活動的參與者詳細清單 |
| | 資料匯出 | `/admin/activity/<int:id>/export` | GET | 下載報名名單 CSV |

---

## 4. 流程設計決策說明

1.  **分流設計**：首頁作為大門，明確區分一般使用者瀏覽與管理端進入點，確保動線清晰。
2.  **即時驗證**：在序列圖中強調了 Flask Route 的驗證步驟，確保進入資料庫前的資料品質。
3.  **確認通知流程**：將郵件與 QR Code 產生視為報名成功後的「副作用」串接，確保使用者能在最短時間內看到成功頁面。
4.  **管理路徑閉環**：主辦方在執行完單一管理任務（如匯出）後，引導回到 Dashboard，維持一致的後台操作邏輯。
