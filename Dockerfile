FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /web
RUN mkdir -p /var/log/django/
ADD . /web
WORKDIR /web
RUN pip install pqi
RUN pqi use douban
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install ./xadmin-django2.zip
