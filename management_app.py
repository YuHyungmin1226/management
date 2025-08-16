from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import csv
import io
import os
import sys
import logging
from flask_wtf import CSRFProtect
# Flask-Limiter 제거 (포터블 버전에서 불필요한 복잡성 제거)
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

# 로깅 설정
def setup_logging():
    """로깅 설정 초기화"""
    log_level = getattr(logging, os.environ.get('LOG_LEVEL', 'INFO').upper())
    log_file_name = os.environ.get('LOG_FILE', 'management.log')
    
    # 로그 파일 경로 설정 (실행 파일과 같은 디렉토리)
    if getattr(sys, 'frozen', False):
        # PyInstaller로 빌드된 경우
        current_dir = os.path.dirname(sys.executable)
    else:
        # 일반 Python 실행의 경우
        current_dir = os.path.dirname(os.path.abspath(__file__))
    
    log_file = os.path.join(current_dir, log_file_name)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# 설정 가져오기
from config import config

# 템플릿 경로 설정: PyInstaller(onefile) 환경에서도 동작하도록 처리
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS  # PyInstaller 임시 해제 경로
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(base_path, 'templates'))

# 환경 설정 적용
config_name = os.environ.get('FLASK_ENV', 'default')
app.config.from_object(config[config_name])

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
# Flask-Limiter 제거 (포터블 버전에서 불필요한 복잡성 제거)
# limiter = Limiter(
#     get_remote_address,
#     app=app,
#     default_limits=["200 per day", "50 per hour"],
#     storage_uri=app.config['RATELIMIT_STORAGE_URI'],
# )

@app.context_processor
def inject_csrf_token():
    from flask_wtf.csrf import generate_csrf
    return dict(csrf_token=generate_csrf)

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
        
        logger.info(f'학생 추가 시도: {student_number} - {name}')
        
        if not student_number or not name:
            logger.warning('학생 추가 실패: 필수 필드 누락')
            flash('학번과 이름을 모두 입력해주세요.', 'error')
            return redirect(url_for('add_student'))
            
        existing_student = Student.query.filter_by(student_number=student_number).first()
        if existing_student:
            logger.warning(f'학생 추가 실패: 중복 학번 {student_number}')
            flash('이미 존재하는 학번입니다.', 'error')
            return redirect(url_for('add_student'))

        new_student = Student(student_number=student_number, name=name)
        db.session.add(new_student)
        db.session.commit()
        logger.info(f'학생 추가 성공: {student_number} - {name}')
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

@app.route('/student/<int:student_id>/delete', methods=['GET', 'POST'])
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

        if not subject or not evaluation_date_str:
            flash('과목과 평가일을 입력해주세요.', 'error')
            return render_template('add_evaluation.html', student=student, today=date.today())

        # 점수가 선택되지 않은 경우 0점으로 처리
        if not score:
            score = 0
        else:
            try:
                score = int(score)
            except ValueError:
                flash('점수 형식이 올바르지 않습니다.', 'error')
                return render_template('add_evaluation.html', student=student, today=date.today())

        try:
            evaluation_date = datetime.strptime(evaluation_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('날짜 형식이 올바르지 않습니다.', 'error')
            return render_template('add_evaluation.html', student=student, today=date.today())

        # 점수 범위 검증 (-5 ~ +5)
        if score < -5 or score > 5:
            flash('점수는 -5에서 5 사이여야 합니다.', 'error')
            return render_template('add_evaluation.html', student=student, today=date.today())

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
    return render_template('add_evaluation.html', student=student, today=date.today())

@app.route('/evaluation/<int:evaluation_id>/edit', methods=['GET', 'POST'])
def edit_evaluation(evaluation_id):
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    student = evaluation.student
    
    if request.method == 'POST':
        subject = request.form.get('subject')
        score = request.form.get('score')
        evaluation_date_str = request.form.get('evaluation_date')
        notes = request.form.get('notes')

        if not subject or not evaluation_date_str:
            flash('과목과 평가일을 입력해주세요.', 'error')
            return render_template('edit_evaluation.html', evaluation=evaluation, student=student, today=date.today())

        # 점수가 선택되지 않은 경우 0점으로 처리
        if not score:
            score = 0
        else:
            try:
                score = int(score)
            except ValueError:
                flash('점수 형식이 올바르지 않습니다.', 'error')
                return render_template('edit_evaluation.html', evaluation=evaluation, student=student, today=date.today())

        try:
            evaluation_date = datetime.strptime(evaluation_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('날짜 형식이 올바르지 않습니다.', 'error')
            return render_template('edit_evaluation.html', evaluation=evaluation, student=student, today=date.today())

        # 점수 범위 검증 (-5 ~ +5)
        if score < -5 or score > 5:
            flash('점수는 -5에서 5 사이여야 합니다.', 'error')
            return render_template('edit_evaluation.html', evaluation=evaluation, student=student, today=date.today())

        # 평가 정보 업데이트
        evaluation.subject = subject
        evaluation.score = score
        evaluation.evaluation_date = evaluation_date
        evaluation.notes = notes

        db.session.commit()
        flash('평가가 성공적으로 수정되었습니다.', 'success')
        return redirect(url_for('view_student', student_id=student.id))
    
    return render_template('edit_evaluation.html', evaluation=evaluation, student=student, today=date.today())

@app.route('/evaluation/<int:evaluation_id>/delete', methods=['POST'])
def delete_evaluation(evaluation_id):
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    student_id = evaluation.student_id
    db.session.delete(evaluation)
    db.session.commit()
    flash('평가가 성공적으로 삭제되었습니다.', 'success')
    return redirect(url_for('view_student', student_id=student_id))

# 학생 CSV 일괄 등록
@app.route('/students/import', methods=['GET', 'POST'])
def import_students():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('CSV 파일을 선택해주세요.', 'error')
            return redirect(url_for('import_students'))

        try:
            content = file.read().decode('utf-8-sig')
            reader = csv.reader(io.StringIO(content))

            rows = list(reader)
            if not rows:
                flash('CSV 파일이 비어 있습니다.', 'error')
                return redirect(url_for('import_students'))

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
            return redirect(url_for('index'))
        except UnicodeDecodeError:
            flash('파일 인코딩을 확인해주세요. UTF-8 형식을 권장합니다.', 'error')
            return redirect(url_for('import_students'))
        except Exception as e:
            flash(f'가져오기 중 오류가 발생했습니다: {str(e)}', 'error')
            return redirect(url_for('import_students'))

    return render_template('import_students.html')


# 특정 학생 평가 CSV 내보내기
@app.route('/student/<int:student_id>/evaluations/export')
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


# 전체 평가 CSV 내보내기
@app.route('/evaluations/export')
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

# 에러 핸들러
@app.errorhandler(404)
def not_found_error(error):
    logger.warning(f'404 에러: {request.url}')
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f'500 에러: {error}')
    db.session.rollback()
    return render_template('500.html'), 500

@app.errorhandler(413)
def too_large(error):
    logger.warning('파일 크기 초과')
    flash('파일 크기가 너무 큽니다.', 'error')
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    logger.info('학생 관리 시스템 시작')
    
    # 데이터베이스 경로 로깅 추가
    logger.info(f'데이터베이스 경로: {app.config["SQLALCHEMY_DATABASE_URI"]}')
    
    try:
        with app.app_context():
            db.create_all()
            logger.info('데이터베이스 초기화 완료')
            
            # 데이터베이스에 학생이 몇 명 있는지 확인
            student_count = Student.query.count()
            logger.info(f'데이터베이스에 학생 {student_count}명이 있습니다')
            
    except Exception as e:
        logger.error(f'데이터베이스 초기화 실패: {e}')
        print(f'데이터베이스 초기화 실패: {e}')
        sys.exit(1)
    
    # 환경 변수에서 포트 설정 가져오기
    port = int(os.environ.get('FLASK_RUN_PORT', 5003))
    
    try:
        logger.info(f'서버 시작: http://localhost:{port}')
        app.run(debug=False, host='0.0.0.0', port=port)
    except Exception as e:
        logger.error(f'서버 시작 실패: {e}')
        print(f'서버 시작 실패: {e}')
        sys.exit(1) 