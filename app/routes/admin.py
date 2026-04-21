from flask import Blueprint, render_template, request, redirect, url_for, flash, session

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# 模擬 login_required 裝飾器，等之後引入 Flask-Login 時再替換
def login_required(f):
    """預留登入驗證裝飾器"""
    # 這裡目前僅寫定義，暫不實作完整邏輯
    return f

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """管理者登入"""
    if request.method == 'POST':
        # TODO: 驗證帳密
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/login.html')

@admin_bp.route('/logout', methods=['POST'])
def logout():
    """執行登出"""
    session.clear()
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """管理控制台 (活動清單)"""
    # TODO: 獲取該管理員的所有活動
    return render_template('admin/dashboard.html')

@admin_bp.route('/activity/new', methods=['GET', 'POST'])
@login_required
def create_activity():
    """建立新活動"""
    if request.method == 'POST':
        # TODO: 儲存活動資料
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/activity_form.html', action="New")

@admin_bp.route('/activity/<int:activity_id>/edit', methods=['GET'])
@login_required
def edit_activity_page(activity_id):
    """編輯活動頁面"""
    return render_template('admin/activity_form.html', action="Edit")

@admin_bp.route('/activity/<int:activity_id>/update', methods=['POST'])
@login_required
def update_activity(activity_id):
    """執行更新活動資料"""
    # TODO: 更新資料庫
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/activity/<int:activity_id>/registrations')
@login_required
def registration_list(activity_id):
    """顯示活動報名清單"""
    # TODO: 查詢該活動所有報名紀錄
    return render_template('admin/registration_list.html')

@admin_bp.route('/activity/<int:activity_id>/export')
@login_required
def export_registrations(activity_id):
    """功能：匯出名單為 CSV"""
    # TODO: 生成並回傳 CSV 檔案
    return "Export CSV content..."
