FROM python:3.11

ARG OPENAI_API_KEY

WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

ENV OPENAI_API_KEY=${OPENAI_API_KEY}

ADD build-knowledge-base.py .
RUN python build-knowledge-base.py

ADD chatbot.py .
CMD ["streamlit", "run", "chatbot.py", "--server.address", "0.0.0.0"]