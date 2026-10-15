# Python 3.10 슬림 이미지 사용
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Cloud Run 기본 포트(8080) 설정 및 uvicorn 실행
ENV PORT=8080
EXPOSE 8080

# 'main:main'을 'main:app' (또는 실제 파일명과 변수명)으로 변경
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
