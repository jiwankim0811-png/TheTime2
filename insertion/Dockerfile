# 파이썬 경량 베이스 이미지 사용
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 소스코드 복사
COPY . .

# Google Cloud Run 포트 환경변수(8080) 대응 및 Uvicorn 실행
ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
