import os
import sys
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image
import filetype
import json

# 파일 업로드 설정
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
THUMBNAIL_SIZE = (300, 300)

# 허용된 파일 타입
ALLOWED_EXTENSIONS = {
    'image': {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'},
    'document': {'pdf', 'doc', 'docx', 'txt', 'rtf'},
    'video': {'mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv'},
    'audio': {'mp3', 'wav', 'flac', 'ogg', 'm4a'},
    'archive': {'zip', 'rar', '7z', 'tar', 'gz'}
}

# 파일 타입별 아이콘
FILE_ICONS = {
    'image': 'bi-image',
    'document': 'bi-file-text',
    'video': 'bi-camera-video',
    'audio': 'bi-music-note',
    'archive': 'bi-archive',
    'unknown': 'bi-file-earmark'
}

def get_file_type(filename):
    """파일 확장자로부터 파일 타입을 반환"""
    if '.' not in filename:
        return 'unknown'
    
    ext = filename.rsplit('.', 1)[1].lower()
    
    for file_type, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return file_type
    
    return 'unknown'

def allowed_file(filename):
    """파일이 허용된 확장자인지 확인"""
    if '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    return any(ext in extensions for extensions in ALLOWED_EXTENSIONS.values())

def get_file_icon(file_type):
    """파일 타입에 따른 아이콘 반환"""
    return FILE_ICONS.get(file_type, FILE_ICONS['unknown'])

def create_upload_folder():
    """업로드 폴더 생성"""
    # 절대 경로로 업로드 폴더 생성 (포터블 버전 대응)
    import sys
    if getattr(sys, 'frozen', False):
        # PyInstaller로 빌드된 경우
        current_dir = os.path.dirname(sys.executable)
    else:
        # 일반 Python 실행의 경우
        current_dir = os.path.dirname(os.path.abspath(__file__))
    
    upload_path = os.path.join(current_dir, UPLOAD_FOLDER)
    
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        print(f"업로드 폴더 생성됨: {upload_path}")
    
    # 하위 폴더들 생성
    for folder in ['images', 'documents', 'videos', 'audio', 'archives']:
        folder_path = os.path.join(upload_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"하위 폴더 생성됨: {folder_path}")

def generate_unique_filename(original_filename):
    """고유한 파일명 생성"""
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if ext:
        return f"{timestamp}_{unique_id}.{ext}"
    else:
        return f"{timestamp}_{unique_id}"

def save_file(file, filename):
    """파일을 저장하고 정보 반환"""
    print(f"save_file 호출됨: {filename}")
    
    # 업로드 폴더 생성
    create_upload_folder()
    
    # 파일 타입 확인
    file_type = get_file_type(filename)
    print(f"파일 타입: {file_type}")
    
    # 고유 파일명 생성
    unique_filename = generate_unique_filename(filename)
    print(f"고유 파일명: {unique_filename}")
    
    # 파일 타입별 저장 경로 설정
    type_folders = {
        'image': 'images',
        'document': 'documents', 
        'video': 'videos',
        'audio': 'audio',
        'archive': 'archives'
    }
    
    # 타입별 폴더 결정
    folder = type_folders.get(file_type, 'documents')
    
    # 파일 경로 설정 (포터블 버전 대응)
    import sys
    if getattr(sys, 'frozen', False):
        # PyInstaller로 빌드된 경우
        current_dir = os.path.dirname(sys.executable)
    else:
        # 일반 Python 실행의 경우
        current_dir = os.path.dirname(os.path.abspath(__file__))
    
    file_path = os.path.join(current_dir, UPLOAD_FOLDER, folder, unique_filename)
    print(f"저장 경로: {file_path}")
    print(f"현재 디렉터리: {current_dir}")
    print(f"파일 타입: {file_type}, 폴더: {folder}")
    
    # 파일 저장 전 해당 폴더가 존재하는지 확인하고 없으면 생성
    folder_path = os.path.dirname(file_path)
    if not os.path.exists(folder_path):
        print(f"폴더가 존재하지 않음, 생성 중: {folder_path}")
        os.makedirs(folder_path, exist_ok=True)
        print(f"폴더 생성 완료: {folder_path}")
    
    # 파일 저장 (더 안전한 방법)
    try:
        # 파일 스트림을 직접 읽어서 저장
        file.seek(0)  # 파일 포인터를 처음으로
        file_content = file.read()
        print(f"파일 내용 읽기 완료: {len(file_content)} bytes")
        
        # 바이너리 모드로 파일 저장
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        print(f"파일 저장 완료: {file_path}")
        
        # 파일 존재 확인
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"파일 존재 확인: {file_size} bytes")
        else:
            print("❌ 파일이 저장되지 않음!")
            raise Exception("파일 저장 실패")
            
    except Exception as e:
        print(f"파일 저장 오류: {e}")
        import traceback
        traceback.print_exc()
        raise
    
    # MIME 타입 확인 (단순화)
    mime_type = 'application/octet-stream'
    if file_type == 'image':
        mime_type = 'image/jpeg' if filename.lower().endswith('.jpg') else 'image/png'
    elif file_type == 'video':
        mime_type = 'video/mp4'
    elif file_type == 'audio':
        mime_type = 'audio/mpeg'
    
    # 이미지 파일인 경우 썸네일 생성
    thumbnail_path = None
    if file_type == 'image':
        try:
            thumbnail_path = create_thumbnail(file_path, unique_filename)
            print(f"썸네일 생성 결과: {thumbnail_path}")
        except Exception as e:
            print(f"썸네일 생성 실패: {e}")
            thumbnail_path = None
    
    # 파일 정보 반환
    file_info = {
        'original_name': filename,
        'saved_name': unique_filename,
        'file_path': file_path,
        'file_type': file_type,
        'file_size': os.path.getsize(file_path),
        'mime_type': mime_type,
        'upload_time': datetime.now().isoformat(),
        'thumbnail_path': thumbnail_path
    }
    
    print(f"반환할 파일 정보: {file_info}")
    return file_info

def create_thumbnail(image_path, filename):
    """이미지 썸네일 생성"""
    try:
        with Image.open(image_path) as img:
            # 이미지 모드 확인 및 변환
            if img.mode in ('RGBA', 'LA'):
                # 투명도가 있는 이미지는 흰색 배경으로 변환
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 썸네일 생성
            img.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
            
            # 썸네일 저장 (포터블 버전 대응)
            thumbnail_name = f"thumb_{filename}"
            if getattr(sys, 'frozen', False):
                # PyInstaller로 빌드된 경우
                current_dir = os.path.dirname(sys.executable)
            else:
                # 일반 Python 실행의 경우
                current_dir = os.path.dirname(os.path.abspath(__file__))
            
            thumbnail_path = os.path.join(current_dir, UPLOAD_FOLDER, 'images', thumbnail_name)
            img.save(thumbnail_path, 'JPEG', quality=85)
            
            return thumbnail_path
    except Exception as e:
        print(f"썸네일 생성 오류: {e}")
        return None

def get_file_size_display(size_bytes):
    """파일 크기를 읽기 쉬운 형태로 변환"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def validate_file(file):
    """파일 유효성 검사"""
    errors = []
    
    # 파일 크기 확인
    if file.content_length and file.content_length > MAX_FILE_SIZE:
        errors.append(f"파일 크기가 너무 큽니다. 최대 {get_file_size_display(MAX_FILE_SIZE)}까지 업로드 가능합니다.")
    
    # 파일 확장자 확인
    if file.filename and not allowed_file(file.filename):
        errors.append("허용되지 않는 파일 형식입니다.")
    
    # 파일 내용 확인 (MIME 타입)
    try:
        file.seek(0)
        file_content = file.read(1024)
        file.seek(0)  # 파일 포인터를 다시 처음으로
        
        # filetype을 사용한 MIME 타입 검증
        kind = filetype.guess(file_content)
        if kind:
            mime_type = kind.mime
            extension = kind.extension
            
            # 허용된 확장자 확인
            allowed_extensions = set()
            for extensions in ALLOWED_EXTENSIONS.values():
                allowed_extensions.update(extensions)
            
            if extension not in allowed_extensions:
                errors.append("파일 내용이 허용되지 않는 형식입니다.")
        else:
            # filetype이 감지하지 못한 경우 확장자로만 확인
            pass
            
    except Exception as e:
        errors.append("파일 검증 중 오류가 발생했습니다.")
    
    return errors

def delete_file(file_path):
    """파일 삭제 (안전한 방법)"""
    try:
        if os.path.exists(file_path):
            # Windows에서 파일이 사용 중일 때를 대비한 안전한 삭제
            import time
            max_retries = 3
            retry_delay = 0.5  # 0.5초 대기
            
            for attempt in range(max_retries):
                try:
                    os.remove(file_path)
                    print(f"✅ 파일 삭제 성공: {file_path}")
                    return True
                except PermissionError as pe:
                    if "다른 프로세스가 사용 중" in str(pe) or "being used by another process" in str(pe):
                        print(f"⚠️ 파일이 사용 중입니다. 재시도 {attempt + 1}/{max_retries}: {file_path}")
                        if attempt < max_retries - 1:
                            time.sleep(retry_delay)
                            continue
                        else:
                            print(f"❌ 파일 삭제 실패 (최대 재시도 초과): {file_path}")
                            return False
                    else:
                        raise
                except OSError as ose:
                    if "다른 프로세스가 사용 중" in str(ose) or "being used by another process" in str(ose):
                        print(f"⚠️ 파일이 사용 중입니다. 재시도 {attempt + 1}/{max_retries}: {file_path}")
                        if attempt < max_retries - 1:
                            time.sleep(retry_delay)
                            continue
                        else:
                            print(f"❌ 파일 삭제 실패 (최대 재시도 초과): {file_path}")
                            return False
                    else:
                        raise
        else:
            print(f"⚠️ 파일이 존재하지 않음: {file_path}")
            return True  # 파일이 없으면 삭제 성공으로 간주
    except Exception as e:
        print(f"❌ 파일 삭제 오류: {file_path} - {e}")
        return False

def get_file_info_from_json(files_json):
    """JSON 문자열에서 파일 정보 추출"""
    if not files_json:
        return []
    
    try:
        return json.loads(files_json)
    except json.JSONDecodeError:
        return [] 