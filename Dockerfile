FROM python:3-alpine
RUN pip install elasticsearch PyGithub

COPY gh-es.py /gh-es.py
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

