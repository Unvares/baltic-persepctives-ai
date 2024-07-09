FROM python:3.11

ARG OPENAI_API_KEY
ARG EMBEDDING_EP

WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD build-knowledge-base.py .
RUN EMBEDDING_EP=$EMBEDDING_EP python build-knowledge-base.py

ENV EMBEDDING_EP ${EMBEDDING_EP}

ADD chatbot.py .
CMD ["streamlit", "run", "chatbot.py", "--server.address", "0.0.0.0"]