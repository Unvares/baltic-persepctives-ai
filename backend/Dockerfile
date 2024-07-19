FROM python:3.11-slim

WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD api.py .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
EXPOSE 8080
