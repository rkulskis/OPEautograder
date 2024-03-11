FROM quay.io/opeffort/nerc:ucsls-S24

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

USER root

RUN chmod 777 $APP_HOME

CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "-k", "gthread", "--threads", "1", "app:app", "--timeout", "600"]
