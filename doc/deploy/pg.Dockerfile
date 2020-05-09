FROM postgres:12.2

ADD ./OA/doc/deploy/pg.table.sql /opt/pg.table.sql
ADD ./OA/doc/deploy/pg.sequence.sql /opt/pg.sequence.sql
ADD ./OA/doc/deploy/pg.start.sh /pg.start.sh

EXPOSE 5432
