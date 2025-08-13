from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# 포터블 버전 대응 - 데이터베이스 경로 설정
if getattr(sys, 'frozen', False):
    # PyInstaller로 빌드된 경우
    current_dir = os.path.dirname(sys.executable)
else:
    # 일반 Python 실행의 경우
    current_dir = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(current_dir, 'management.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 데이터베이스 모델
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    evaluations = db.relationship('Evaluation', backref='student', lazy=True, cascade='all, delete-orphan')

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float)
    evaluation_date = db.Column(db.Date)
    notes = db.Column(db.Text)

@app.template_filter('format_date')
def format_date_filter(value, format='%Y-%m-%d'):
    if value is None:
        return ""
    return value.strftime(format)

@app.route('/')
def index():
    query = request.args.get('q', '').strip()
    students_query = Student.query
    if query:
        like = f"%{query}%"
        students_query = students_query.filter(
            or_(
                Student.student_number.like(like),
                Student.name.like(like)
            )
        )
    students = students_query.order_by(Student.student_number).all()
    return render_template('index.html', students=students, q=query)

@app.route('/student/new', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_number = request.form.get('student_number')
        name = request.form.get('name')
        
        if not student_number or not name:
            flash('학번과 이름을 모두 입력해주세요.', 'error')
            return redirect(url_for('add_student'))
            
        existing_student = Student.query.filter_by(student_number=student_number).first()
        if existing_student:
            flash('이미 존재하는 학번입니다.', 'error')
            return redirect(url_for('add_student'))

        new_student = Student(student_number=student_number, name=name)
        db.session.add(new_student)
        db.session.commit()
        flash('학생이 성공적으로 추가되었습니다.', 'success')
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/student/<int:student_id>')
def view_student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('view_student.html', student=student)

@app.route('/student/<int:student_id>/edit', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        new_student_number = request.form.get('student_number')
        new_name = request.form.get('name')
        
        if not new_student_number or not new_name:
            flash('학번과 이름을 모두 입력해주세요.', 'error')
            return render_template('edit_student.html', student=student)

        # 학번 고유성 검증: 본인 이외 동일 학번 존재 시 오류
        existing_student = Student.query.filter(
            Student.student_number == new_student_number,
            Student.id != student.id
        ).first()
        if existing_student:
            flash('이미 존재하는 학번입니다.', 'error')
            return render_template('edit_student.html', student=student)

        student.student_number = new_student_number
        student.name = new_name

        db.session.commit()
        flash('학생 정보가 성공적으로 수정되었습니다.', 'success')
        return redirect(url_for('view_student', student_id=student.id))
    return render_template('edit_student.html', student=student)

@app.route('/student/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('학생이 성공적으로 삭제되었습니다.', 'success')
    return redirect(url_for('index'))

@app.route('/student/<int:student_id>/evaluation/new', methods=['GET', 'POST'])
def add_evaluation(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        subject = request.form.get('subject')
        score = request.form.get('score')
        evaluation_date_str = request.form.get('evaluation_date')
        notes = request.form.get('notes')

        if not subject or not score or not evaluation_date_str:
            flash('과목, 점수, 평가일을 모두 입력해주세요.', 'error')
            return render_template('add_evaluation.html', student=student, today=datetime.utcnow().date())

        try:
            score = int(score)
            evaluation_date = datetime.strptime(evaluation_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('점수 또는 날짜 형식이 올바르지 않습니다.', 'error')
            return render_template('add_evaluation.html', student=student, today=datetime.utcnow().date())

        # 점수 범위 검증 (-5 ~ +5)
        if score < -5 or score > 5:
            flash('점수는 -5에서 5 사이여야 합니다.', 'error')
            return render_template('add_evaluation.html', student=student, today=datetime.utcnow().date())

        new_evaluation = Evaluation(
            subject=subject,
            score=score,
            evaluation_date=evaluation_date,
            notes=notes,
            student_id=student_id
        )
        db.session.add(new_evaluation)
        db.session.commit()
        flash('평가가 성공적으로 추가되었습니다.', 'success')
        return redirect(url_for('view_student', student_id=student_id))
    return render_template('add_evaluation.html', student=student, today=datetime.utcnow().date())

@app.route('/evaluation/<int:evaluation_id>/delete', methods=['POST'])
def delete_evaluation(evaluation_id):
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    student_id = evaluation.student_id
    db.session.delete(evaluation)
    db.session.commit()
    flash('평가가 성공적으로 삭제되었습니다.', 'success')
    return redirect(url_for('view_student', student_id=student_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000) 