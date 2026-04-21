# 路由設計 (ROUTES DESIGN)

本文件定義系統的所有 URL 路徑、HTTP 方法及對應的處理邏輯，作為前後端開發的對接規範。

## 1. 路由總覽

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **公開頁面** | | | | |
| 活動列表 (首頁) | GET | `/` | `index.html` | 顯示所有開放報名的活動 |
| 活動詳情頁 | GET | `/activity/<id>` | `activity_detail.html` | 顯示單一活動詳情與報名表單 |
| 提交報名表單 | POST | `/activity/<id>/register` | — | 驗證並儲存報名資料，完成後跳轉 |
| 報名成功頁面 | GET | `/registration/success/<token>`| `success.html` | 顯示報名成功訊息與電子票券 |
| **管理後台** | | | | |
| 管理員登入頁 | GET | `/admin/login` | `admin/login.html` | 顯示管理者登入表單 |
| 執行登入 | POST | `/admin/login` | — | 驗證帳密，建立 Session |
| 執行登出 | POST | `/admin/logout` | — | 清除 Session |
| 管理控制台 | GET | `/admin/dashboard` | `admin/dashboard.html` | 顯示該管理員擁有的活動清單 |
| 新增活動頁面 | GET | `/admin/activity/new` | `admin/activity_form.html` | 顯示建立活動的表單 |
| 儲存新活動 | POST | `/admin/activity/new` | — | 儲存活動資料至 DB |
| 編輯活動頁面 | GET | `/admin/activity/<id>/edit` | `admin/activity_form.html` | 顯示現有活動的編輯表單 |
| 更新活動資料 | POST | `/admin/activity/<id>/update` | — | 更新活動內容 |
| 報名名單管理 | GET | `/admin/activity/<id>/registrations`| `admin/registration_list.html`| 顯示該活動的所有報名者 |
| 匯出報名名單 | GET | `/admin/activity/<id>/export` | — | 下載 CSV 格式的報名清單 |

---

## 2. 詳細路由說明

### 2.1 參與者報名流程

#### `POST /activity/<id>/register`
- **輸入**: 姓名 (name), Email (email), 電話 (phone), 自訂回答 (JSON string/Form data)。
- **處理**: 檢查名額限制 -> 呼叫 `Registration.create()` -> 產出隨機 `qr_code_token` -> 觸發模擬 Email 通知。
- **輸出**: 重導向至 `/registration/success/<token>`。
- **錯誤處理**: 名額滿或格式錯誤時，導回詳情頁並顯示錯誤訊息。

---

### 2.2 主辦方管理流程

#### `GET /admin/dashboard`
- **處理**: 呼叫 `Activity.query.filter_by(user_id=session['user_id'])`。
- **預留權限**: `@login_required`。

#### `GET /admin/activity/<id>/export`
- **處理**: 查詢該活動的所有 `Registration` -> 轉換為 CSV 流。
- **輸出**: 檔案下載 (Content-Type: text/csv)。

---

## 3. Jinja2 模板清單

所有模板均繼承 `base.html`，位於 `app/templates/` 目錄。

- `base.html`: 包含標頭 (Nav)、導覽列與共用 CSS/JS。
- `index.html`: 活動列表網格。
- `activity_detail.html`: 活動文案與動態生成的報名表單。
- `success.html`: 報名成功確認與票券顯示。
- `admin/login.html`: 登入介面。
- `admin/dashboard.html`: 活動列表與簡易數據。
- `admin/activity_form.html`: 用於「新增」與「編輯」活動的共用表單。
- `admin/registration_list.html`: 參與者管理表格。
