FROM python

RUN useradd cadpython

WORKDIR /home/cadpython

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql cryptography


COPY app app
COPY migrations migrations
COPY cadpython.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP cadpython.py

RUN chown -R cadpython:cadpython ./
USER cadpython

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]