FROM python:3.11-slim

ARG API_KEY

WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

ENV API_KEY ${API_KEY}

ADD . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
EXPOSE 8080
