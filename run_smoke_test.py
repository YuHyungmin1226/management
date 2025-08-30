import sys
from datetime import datetime, UTC

import os
os.environ['FLASK_ENV'] = 'testing'

from management_app import app, db, Student, Evaluation, User


def assert_in(text, haystack, label, failures):
    if text not in haystack:
        failures.append(f"[{label}] 기대 문구 누락: {text}")


def main():
    failures = []

    # 테스트 설정: 인메모리 DB 사용
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['RATELIMIT_ENABLED'] = False

    with app.app_context():
        db.drop_all()
        db.create_all()

        # 테스트용 사용자 생성
        test_user = User(username='testuser', email='test@example.com')
        test_user.set_password('testpass')
        db.session.add(test_user)
        db.session.commit()

        client = app.test_client()

        # 1) 로그인 테스트
        r = client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        }, follow_redirects=True)
        if r.status_code != 200:
            failures.append(f"[login] status {r.status_code}")
        assert_in('testuser님, 환영합니다!', r.get_data(as_text=True), 'login', failures)

        # 2) 인덱스 페이지 (로그인 후)
        r = client.get('/')
        if r.status_code != 200:
            failures.append(f"[index] status {r.status_code}")
        assert_in('학생 목록', r.get_data(as_text=True), 'index', failures)

        # 3) 학생 추가 성공
        r = client.post('/student/new', data={
            'student_number': 'S001',
            'name': '홍길동'
        }, follow_redirects=True)
        if r.status_code != 200:
            failures.append(f"[add_student] status {r.status_code}")
        assert_in('학생이 성공적으로 추가되었습니다.', r.get_data(as_text=True), 'add_student', failures)

        # 학생 객체 조회 (이후 테스트에서 사용)
        s1 = Student.query.filter_by(student_number='S001').first()
        if not s1:
            failures.append('[db] 학생 S001 조회 실패(초기)')

        # 4) 검색: 이름으로
        r = client.get('/?q=%ED%99%8D%EA%B8%B8%EB%8F%99')
        if r.status_code != 200:
            failures.append(f"[search_name] status {r.status_code}")
        assert_in('홍길동', r.get_data(as_text=True), 'search_name', failures)

        # 5) 검색: 학번으로
        r = client.get('/?q=S001')
        if r.status_code != 200:
            failures.append(f"[search_number] status {r.status_code}")
        assert_in('S001', r.get_data(as_text=True), 'search_number', failures)

        # 6) CSV 전체 평가 다운로드 (학생 추가 직후에도 빈 CSV여야 함)
        r = client.get('/evaluations/export')
        if r.status_code != 200 or 'text/csv' not in r.headers.get('Content-Type', ''):
            failures.append('[export_all] CSV 응답 오류')
        
        # 7) 학생 평가 다운로드 (평가 추가 후)
        if s1:
            r = client.get(f'/student/{s1.id}/evaluations/export')
            if r.status_code != 200 or 'text/csv' not in r.headers.get('Content-Type', ''):
                failures.append('[export_student] CSV 응답 오류')

        # 8) 학생 추가 중복 오류
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

        # 9) 학생 상세 보기
        r = client.get(f'/student/{s1.id}')
        if r.status_code != 200:
            failures.append(f"[view_student] status {r.status_code}")

        # 10) 평가 추가 성공 (-5~5 정수)
        today = datetime.now(UTC).strftime('%Y-%m-%d')
        r = client.post(f'/student/{s1.id}/evaluation/new', data={
            'subject': '수학',
            'score': '3',
            'evaluation_date': today,
            'notes': '잘함'
        }, follow_redirects=True)
        assert_in('평가가 성공적으로 추가되었습니다.', r.get_data(as_text=True), 'add_evaluation', failures)

        # 11) 점수 범위 오류
        r = client.post(f'/student/{s1.id}/evaluation/new', data={
            'subject': '국어',
            'score': '6',
            'evaluation_date': today,
            'notes': ''
        }, follow_redirects=True)
        assert_in('점수는 -5에서 5 사이여야 합니다.', r.get_data(as_text=True), 'score_range', failures)

        # 12) 평가 삭제
        ev = Evaluation.query.filter_by(student_id=s1.id).first()
        if not ev:
            failures.append('[db] 평가 조회 실패')
        else:
            r = client.post(f'/evaluation/{ev.id}/delete', follow_redirects=True)
            assert_in('평가가 성공적으로 삭제되었습니다.', r.get_data(as_text=True), 'delete_evaluation', failures)

        # 13) 학생 수정 성공
        r = client.post(f'/student/{s1.id}/edit', data={
            'student_number': 'S001',
            'name': '홍길동2'
        }, follow_redirects=True)
        assert_in('학생 정보가 성공적으로 수정되었습니다.', r.get_data(as_text=True), 'edit_student', failures)

        # 14) 학번 중복 검증(편집)
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

        # 15) 학생 삭제
        r = client.post(f'/student/{s1.id}/delete', follow_redirects=True)
        assert_in('학생이 성공적으로 삭제되었습니다.', r.get_data(as_text=True), 'delete_student', failures)

        # 16) 로그아웃 테스트
        r = client.get('/logout', follow_redirects=True)
        if r.status_code != 200:
            failures.append(f"[logout] status {r.status_code}")
        assert_in('로그아웃되었습니다.', r.get_data(as_text=True), 'logout', failures)

        # 17) 로그인 없이 접근 시도 (리다이렉트 확인)
        r = client.get('/', follow_redirects=False)
        if r.status_code != 302:  # 리다이렉트
            failures.append(f"[unauthorized_access] status {r.status_code}")

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


