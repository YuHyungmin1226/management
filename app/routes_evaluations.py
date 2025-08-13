from __future__ import annotations

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
import csv
import io

from .extensions import db, limiter
from .models import Student, Evaluation


bp = Blueprint('evaluations', __name__)


@bp.route('/student/<int:student_id>/evaluation/new', methods=['GET', 'POST'])
@limiter.limit("60/hour")
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

        if score < -5 or score > 5:
            flash('점수는 -5에서 5 사이여야 합니다.', 'error')
            return render_template('add_evaluation.html', student=student, today=datetime.utcnow().date())

        new_evaluation = Evaluation(
            subject=subject,
            score=score,
            evaluation_date=evaluation_date,
            notes=notes,
            student_id=student_id,
        )
        db.session.add(new_evaluation)
        db.session.commit()
        flash('평가가 성공적으로 추가되었습니다.', 'success')
        return redirect(url_for('students.view_student', student_id=student_id))
    return render_template('add_evaluation.html', student=student, today=datetime.utcnow().date())


@bp.route('/evaluation/<int:evaluation_id>/delete', methods=['POST'])
@limiter.limit("60/hour")
def delete_evaluation(evaluation_id):
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    student_id = evaluation.student_id
    db.session.delete(evaluation)
    db.session.commit()
    flash('평가가 성공적으로 삭제되었습니다.', 'success')
    return redirect(url_for('students.view_student', student_id=student_id))


@bp.route('/students/import', methods=['GET', 'POST'])
@limiter.limit("10/minute")
def import_students():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('CSV 파일을 선택해주세요.', 'error')
            return redirect(url_for('evaluations.import_students'))

        try:
            content = file.read().decode('utf-8-sig')
            reader = csv.reader(io.StringIO(content))
            rows = list(reader)
            if not rows:
                flash('CSV 파일이 비어 있습니다.', 'error')
                return redirect(url_for('evaluations.import_students'))

            start_index = 0
            header = [h.strip().lower() for h in rows[0]] if rows else []
            if header and (header == ['student_number', 'name'] or header == ['학번', '이름']):
                start_index = 1

            total_count = 0
            added_count = 0
            skipped_count = 0

            for row in rows[start_index:]:
                total_count += 1
                if len(row) < 2:
                    skipped_count += 1
                    continue
                student_number = str(row[0]).strip()
                name = str(row[1]).strip()
                if not student_number or not name:
                    skipped_count += 1
                    continue
                existing = Student.query.filter_by(student_number=student_number).first()
                if existing:
                    skipped_count += 1
                    continue
                db.session.add(Student(student_number=student_number, name=name))
                added_count += 1

            db.session.commit()
            flash(f'CSV 처리 완료: 총 {total_count}건, 추가 {added_count}건, 건너뜀 {skipped_count}건', 'success')
            return redirect(url_for('students.index'))
        except UnicodeDecodeError:
            flash('파일 인코딩을 확인해주세요. UTF-8 형식을 권장합니다.', 'error')
            return redirect(url_for('evaluations.import_students'))
        except Exception as e:  # noqa: BLE001
            flash(f'가져오기 중 오류가 발생했습니다: {str(e)}', 'error')
            return redirect(url_for('evaluations.import_students'))

    return render_template('import_students.html')


@bp.route('/student/<int:student_id>/evaluations/export')
def export_student_evaluations(student_id):
    student = Student.query.get_or_404(student_id)
    output = io.StringIO(newline='')
    writer = csv.writer(output)
    writer.writerow(['student_number', 'name', 'subject', 'score', 'evaluation_date', 'notes'])
    for ev in student.evaluations:
        writer.writerow([
            student.student_number,
            student.name,
            ev.subject or '',
            ev.score if ev.score is not None else '',
            ev.evaluation_date.strftime('%Y-%m-%d') if ev.evaluation_date else '',
            ev.notes or ''
        ])

    csv_data = '\ufeff' + output.getvalue()
    response = make_response(csv_data)
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    filename = f"evaluations_{student.student_number}.csv"
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@bp.route('/evaluations/export')
def export_all_evaluations():
    output = io.StringIO(newline='')
    writer = csv.writer(output)
    writer.writerow(['student_number', 'name', 'subject', 'score', 'evaluation_date', 'notes'])

    students = Student.query.order_by(Student.student_number).all()
    for student in students:
        for ev in student.evaluations:
            writer.writerow([
                student.student_number,
                student.name,
                ev.subject or '',
                ev.score if ev.score is not None else '',
                ev.evaluation_date.strftime('%Y-%m-%d') if ev.evaluation_date else '',
                ev.notes or ''
            ])

    csv_data = '\ufeff' + output.getvalue()
    response = make_response(csv_data)
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename="evaluations_all.csv"'
    return response


