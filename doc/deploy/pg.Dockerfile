FROM postgres:12.2

ADD ./OA/doc/deploy/pg.sql /opt/pg.sql
ADD ./OA/doc/deploy/pg.start.sh /pg.start.sh

EXPOSE 5432
