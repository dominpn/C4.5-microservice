FROM python:3.7

ENV DASH_DEBUG_MODE True

COPY requirements.txt requirements.txt

RUN set -ex && \
    pip install -r requirements.txt

EXPOSE 8050

COPY ./app /app

WORKDIR /app

CMD ["python", "app.py"]