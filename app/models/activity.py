from datetime import datetime
from .database import db

class Activity(db.Model):
    """活動模型"""
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    registration_deadline = db.Column(db.DateTime, nullable=False)
    max_slots = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default='draft') # draft, published, closed
    custom_form_fields = db.Column(db.JSON) # 存儲為 JSON 格式
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 建立與報名紀錄的關聯
    registrations = db.relationship('Registration', backref='activity', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Activity {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'registration_deadline': self.registration_deadline.isoformat(),
            'max_slots': self.max_slots,
            'status': self.status,
            'custom_form_fields': self.custom_form_fields,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def create(cls, user_id, title, start_time, end_time, registration_deadline, **kwargs):
        activity = cls(
            user_id=user_id,
            title=title,
            start_time=start_time,
            end_time=end_time,
            registration_deadline=registration_deadline,
            **kwargs
        )
        db.session.add(activity)
        db.session.commit()
        return activity

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, activity_id):
        return cls.query.get(activity_id)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
