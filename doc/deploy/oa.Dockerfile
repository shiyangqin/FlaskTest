FROM centos:centos7

ADD ./OA /opt/OA

RUN yum install -y gcc openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel libffi-devel tk-devel wget curl-devel make \
    && wget -P /opt https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tar.xz \
    && tar -xvJf /opt/Python-3.8.2.tar.xz -C /opt \
    && mkdir /usr/local/python3 \
    && /opt/Python-3.8.2/configure --prefix=/usr/local/python3 \
    && make \
    && make install \
    && ln -s /usr/local/python3/bin/python3 /usr/local/bin/python3 \
    && ln -s /usr/local/python3/bin/pip3 /usr/local/bin/pip3 \
    && rm -rf /opt/Python* \
    && yum install -y python-devel postgresql-devel \
    && pip3 install -r /opt/OA/doc/deploy/r.txt \
    && pip3 install gunicorn \
    && pip3 install gevent \
    && yum install -y epel-release \
    && yum install -y supervisor \
    && yum install -y nginx \
    && mv /opt/OA/doc/deploy/oa.start.sh /oa.start.sh \
    && mv /opt/OA/doc/deploy/nginx.conf /etc/nginx/nginx.conf \
    && mv /opt/OA/doc/deploy/supervisor.ini /etc/supervisord.d/supervisor.ini \
    && chmod 777 /oa.start.sh

EXPOSE 80
