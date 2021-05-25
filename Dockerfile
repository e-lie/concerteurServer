FROM python:3.8

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

WORKDIR /concerteur_server

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY --chown=uwsgi:uwsgi . /concerteur_server

COPY boot.sh /
RUN chmod a+x /boot.sh

# ENV
EXPOSE 9090
USER uwsgi

CMD ["/boot.sh"]
