FROM postgres:12.2

ADD ./OA/doc/deploy/pg.oa_data.sql /opt/pg.oa_data.sql
ADD ./OA/doc/deploy/pg.start.sh /pg.start.sh

EXPOSE 5432
