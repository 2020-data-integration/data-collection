FROM python:3.7.4

WORKDIR /usr/app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY stock/cronjob.py cronjob.py

ENTRYPOINT ["python", "cronjob.py"]