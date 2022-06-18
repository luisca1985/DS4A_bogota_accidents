FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

ARG APP_HOME=/app

WORKDIR ${APP_HOME}

# Requirements are installed here to ensure they will be cached.
COPY requirements.txt ${APP_HOME}/requirements.txt

# Dependencies
RUN pip3 install -r requirements.txt

# copy application code to WORKDIR
COPY . ${APP_HOME}

CMD ["python3","app.py"]