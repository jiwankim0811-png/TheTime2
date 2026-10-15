FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
EXPOSE 8080

# main:app 대신 app:app으로 변경 (app.py 파일을 실행하기 위함)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
