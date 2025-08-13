from __future__ import annotations

from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import or_

from .extensions import db, limiter
from .models import Student


bp = Blueprint('students', __name__)


@bp.app_template_filter('format_date')
def format_date_filter(value, format='%Y-%m-%d'):
    if value is None:
        return ""
    return value.strftime(format)


@bp.route('/')
def index():
    query = request.args.get('q', '').strip()
    students_query = Student.query
    if query:
        like = f"%{query}%"
        students_query = students_query.filter(
            or_(Student.student_number.like(like), Student.name.like(like))
        )
    students = students_query.order_by(Student.student_number).all()
    return render_template('index.html', students=students, q=query)


@bp.route('/student/new', methods=['GET', 'POST'])
@limiter.limit("20/hour")
def add_student():
    if request.method == 'POST':
        student_number = request.form.get('student_number')
        name = request.form.get('name')

        if not student_number or not name:
            flash('학번과 이름을 모두 입력해주세요.', 'error')
            return redirect(url_for('students.add_student'))

        existing_student = Student.query.filter_by(student_number=student_number).first()
        if existing_student:
            flash('이미 존재하는 학번입니다.', 'error')
            return redirect(url_for('students.add_student'))

        new_student = Student(student_number=student_number, name=name)
        db.session.add(new_student)
        db.session.commit()
        flash('학생이 성공적으로 추가되었습니다.', 'success')
        return redirect(url_for('students.index'))
    return render_template('add_student.html')


@bp.route('/student/<int:student_id>')
def view_student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('view_student.html', student=student)


@bp.route('/student/<int:student_id>/edit', methods=['GET', 'POST'])
@limiter.limit("30/hour")
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        new_student_number = request.form.get('student_number')
        new_name = request.form.get('name')

        if not new_student_number or not new_name:
            flash('학번과 이름을 모두 입력해주세요.', 'error')
            return render_template('edit_student.html', student=student)

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
        return redirect(url_for('students.view_student', student_id=student.id))
    return render_template('edit_student.html', student=student)


@bp.route('/student/<int:student_id>/delete', methods=['POST'])
@limiter.limit("30/hour")
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('학생이 성공적으로 삭제되었습니다.', 'success')
    return redirect(url_for('students.index'))


