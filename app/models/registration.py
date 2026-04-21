from datetime import datetime
from .database import db

class Registration(db.Model):
    """報名紀錄模型"""
    __tablename__ = 'registrations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    custom_responses = db.Column(db.JSON) # 存儲為 JSON 格式
    qr_code_token = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='confirmed') # confirmed, attended, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Registration {self.name} for Activity {self.activity_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'activity_id': self.activity_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'custom_responses': self.custom_responses,
            'qr_code_token': self.qr_code_token,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def create(cls, activity_id, name, email, qr_code_token, **kwargs):
        registration = cls(
            activity_id=activity_id,
            name=name,
            email=email,
            qr_code_token=qr_code_token,
            **kwargs
        )
        db.session.add(registration)
        db.session.commit()
        return registration

    @classmethod
    def get_by_activity(cls, activity_id):
        return cls.query.filter_by(activity_id=activity_id).all()

    @classmethod
    def get_by_token(cls, token):
        return cls.query.filter_by(qr_code_token=token).first()

    def update_status(self, new_status):
        self.status = new_status
        db.session.commit()
        return self
