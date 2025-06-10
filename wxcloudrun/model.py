from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Counter(db.Model):
    __tablename__ = 'Counters'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    count = db.Column(db.Integer, nullable=False, default=1)
    createdAt = db.Column(db.DateTime, server_default=db.func.now())
    updatedAt = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now()) 