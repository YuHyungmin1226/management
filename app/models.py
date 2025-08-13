from __future__ import annotations

from datetime import datetime
from .extensions import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    evaluations = db.relationship('Evaluation', backref='student', lazy=True, cascade='all, delete-orphan')


class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False, index=True)
    subject = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer)  # -5 ~ 5
    evaluation_date = db.Column(db.Date, index=True)
    notes = db.Column(db.Text)


