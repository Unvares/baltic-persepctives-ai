FROM python:3.11

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

ENV STREAMLIT_THEME_PRIMARY_COLOR "#E40039"
ENV STREAMLIT_THEME_BASE "light"
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS "false"
ENV STREAMLIT_LOGGER_MESSAGE_FORMAT "%(message)s"

CMD ["streamlit", "run", "main.py", "--server.fileWatcherType", "none", "--logger.level", "debug"]