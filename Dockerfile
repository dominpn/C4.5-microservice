FROM python:3.7

ENV DASH_DEBUG_MODE True

COPY requirements.txt requirements.txt

RUN set -ex && \
    pip install -r requirements.txt

EXPOSE 8050

COPY app.py app.py
COPY ./bin /bin
COPY ./parser /parser

CMD ["python", "app.py"]