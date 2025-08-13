import sys
from datetime import datetime

from management_app import app, db, Student, Evaluation


def assert_in(text, haystack, label, failures):
    if text not in haystack:
        failures.append(f"[{label}] 기대 문구 누락: {text}")


def main():
    failures = []

    # 테스트 설정: 인메모리 DB 사용
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.drop_all()
        db.create_all()

        client = app.test_client()

        # 1) 인덱스 페이지
        r = client.get('/')
        if r.status_code != 200:
            failures.append(f"[index] status {r.status_code}")
        assert_in('학생 목록', r.get_data(as_text=True), 'index', failures)

        # 2) 학생 추가 성공
        r = client.post('/student/new', data={
            'student_number': 'S001',
            'name': '홍길동'
        }, follow_redirects=True)
        if r.status_code != 200:
            failures.append(f"[add_student] status {r.status_code}")
        assert_in('학생이 성공적으로 추가되었습니다.', r.get_data(as_text=True), 'add_student', failures)

        # 3) 학생 추가 중복 오류
        r = client.post('/student/new', data={
            'student_number': 'S001',
            'name': '아무개'
        }, follow_redirects=True)
        assert_in('이미 존재하는 학번입니다.', r.get_data(as_text=True), 'add_student_duplicate', failures)

        s1 = Student.query.filter_by(student_number='S001').first()
        if not s1:
            failures.append('[db] 학생 S001 조회 실패')
            print_result(failures)
            return 1

        # 4) 학생 상세 보기
        r = client.get(f'/student/{s1.id}')
        if r.status_code != 200:
            failures.append(f"[view_student] status {r.status_code}")

        # 5) 평가 추가 성공
        today = datetime.utcnow().strftime('%Y-%m-%d')
        r = client.post(f'/student/{s1.id}/evaluation/new', data={
            'subject': '수학',
            'score': '95',
            'evaluation_date': today,
            'notes': '잘함'
        }, follow_redirects=True)
        assert_in('평가가 성공적으로 추가되었습니다.', r.get_data(as_text=True), 'add_evaluation', failures)

        # 6) 점수 범위 오류
        r = client.post(f'/student/{s1.id}/evaluation/new', data={
            'subject': '국어',
            'score': '105',
            'evaluation_date': today,
            'notes': ''
        }, follow_redirects=True)
        assert_in('점수는 0에서 100 사이여야 합니다.', r.get_data(as_text=True), 'score_range', failures)

        # 7) 평가 삭제
        ev = Evaluation.query.filter_by(student_id=s1.id).first()
        if not ev:
            failures.append('[db] 평가 조회 실패')
        else:
            r = client.post(f'/evaluation/{ev.id}/delete', follow_redirects=True)
            assert_in('평가가 성공적으로 삭제되었습니다.', r.get_data(as_text=True), 'delete_evaluation', failures)

        # 8) 학생 수정 성공
        r = client.post(f'/student/{s1.id}/edit', data={
            'student_number': 'S001',
            'name': '홍길동2'
        }, follow_redirects=True)
        assert_in('학생 정보가 성공적으로 수정되었습니다.', r.get_data(as_text=True), 'edit_student', failures)

        # 9) 학번 중복 검증(편집)
        r = client.post('/student/new', data={
            'student_number': 'S002',
            'name': '김철수'
        }, follow_redirects=True)
        s2 = Student.query.filter_by(student_number='S002').first()
        if not s2:
            failures.append('[db] 학생 S002 생성 실패')
        else:
            r = client.post(f'/student/{s2.id}/edit', data={
                'student_number': 'S001',
                'name': '김철수'
            }, follow_redirects=True)
            assert_in('이미 존재하는 학번입니다.', r.get_data(as_text=True), 'edit_duplicate', failures)

        # 10) 학생 삭제
        r = client.post(f'/student/{s1.id}/delete', follow_redirects=True)
        assert_in('학생이 성공적으로 삭제되었습니다.', r.get_data(as_text=True), 'delete_student', failures)

    print_result(failures)
    return 0 if not failures else 1


def print_result(failures):
    if failures:
        print('스모크 테스트 실패:')
        for f in failures:
            print(' -', f)
    else:
        print('스모크 테스트 통과: 모든 핵심 경로 OK')


if __name__ == '__main__':
    sys.exit(main())


