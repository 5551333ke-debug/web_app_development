from .main import main_bp
from .admin import admin_bp

# 導出 Blueprints，方便 app.py 註冊
__all__ = ['main_bp', 'admin_bp']
