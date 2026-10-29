# ==============================================================================
# Google Cloud Run 배포용 Dockerfile
# Python 3.12 Slim 이미지를 기반으로 경량화 및 보안성을 갖춘 컨테이너를 빌드합니다.
# ==============================================================================

FROM python:3.12-slim

# 파이썬 출력 버퍼링 비활성화 (로그가 Cloud Run 콘솔에 실시간 출력되도록 설정)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 애플리케이션 작업 디렉토리 설정
WORKDIR /app

# 종속성 파일 복사 및 설치 (도커 레이어 캐싱 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 코드 복사
COPY . .

# Cloud Run은 환경 변수 PORT(기본값 8080)를 동적으로 할당합니다.
# 기본 포트 노출 선언 (문서화 목적)
EXPOSE 8080

# Uvicorn 서버 실행 명령어:
# Cloud Run의 ${PORT:-8080} 환경변수를 바인딩하여 수신 대기합니다.
CMD ["sh", "-c", "exec uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1"]

