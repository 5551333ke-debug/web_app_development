-- 活動報名系統資料庫 Schema (SQLite)

-- 1. 使用者 (管理者) 表
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    email TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. 活動表
CREATE TABLE activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    location TEXT,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    registration_deadline DATETIME NOT NULL,
    max_slots INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL CHECK (status IN ('draft', 'published', 'closed')),
    custom_form_fields TEXT, -- 存儲 JSON 格式
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- 3. 報名紀錄表
CREATE TABLE registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    custom_responses TEXT, -- 存儲 JSON 格式
    qr_code_token TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL CHECK (status IN ('confirmed', 'attended', 'cancelled')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (activity_id) REFERENCES activities (id) ON DELETE CASCADE
);

-- 索引：提高查詢效能
CREATE INDEX idx_activities_user ON activities(user_id);
CREATE INDEX idx_registrations_activity ON registrations(activity_id);
CREATE INDEX idx_registrations_token ON registrations(qr_code_token);
