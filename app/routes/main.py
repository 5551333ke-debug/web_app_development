from flask import Blueprint, render_template, request, redirect, url_for, flash

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """顯示首頁活動列表"""
    # TODO: 獲取所有公開活動並傳入模板
    return render_template('index.html')

@main_bp.route('/activity/<int:activity_id>')
def activity_detail(activity_id):
    """顯示活動詳情與報名表單"""
    # TODO: 根據 ID 查詢活動
    return render_template('activity_detail.html')

@main_bp.route('/activity/<int:activity_id>/register', methods=['POST'])
def register(activity_id):
    """處理活動報名提交"""
    # TODO: 驗證表單資料，儲存至資料庫
    # 成功後重導向至成功頁面
    return redirect(url_for('main.success', token='mock-token'))

@main_bp.route('/registration/success/<token>')
def success(token):
    """顯示報名成功頁面與電子票券"""
    # TODO: 根據 token 查詢報名紀錄
    return render_template('success.html')
