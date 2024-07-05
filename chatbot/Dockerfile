FROM python:3.11

WORKDIR /app

ADD requirements.txt ./
RUN pip install -r requirements.txt

ADD chatbot.py ./
CMD ["streamlit", "run", "chatbot.py", "--server.address", "0.0.0.0"]