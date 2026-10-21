# 파이썬 3.10 슬림 경량화 이미지 사용
FROM python:3.10-slim

# 컨테이너 내 작업 디렉토리 설정
WORKDIR /app

# 파이썬 바이트코드 생성 방지 및 버퍼링 없는 로그 출력 설정
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 코드 복사
COPY . .

# Cloud Run에서 사용하는 8080 포트 노출
EXPOSE 8080

# Uvicorn 웹 서버 실행 (0.0.0.0 바인딩 및 PORT 환경변수 대응)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
