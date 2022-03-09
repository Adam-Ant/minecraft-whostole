FROM python:alpine

LABEL maintainer="Adam Dodman <hello@adam-ant.co.uk>" \
      org.label-schema.vendor="Adam-Ant" \
      org.label-schema.name="WhoStole" \
      org.label-schema.url="https://github.com/Adam-Ant/minecraft-whostole" \
      org.label-schema.description="Telegram bot for reading player inventories" \
      org.label-schema.version="0.1"

COPY requirements.txt main.py /

RUN pip3 install -r /requirements.txt

VOLUME /world

ENTRYPOINT ["python3", "-u", "/main.py"]