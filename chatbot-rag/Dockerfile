FROM python:3.11

WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD build-knowledge-base.py .
RUN python build-knowledge-base.py

ADD chatbot.py .
CMD ["streamlit", "run", "chatbot.py", "--server.address", "0.0.0.0"]