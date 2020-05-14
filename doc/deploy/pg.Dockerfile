FROM postgres:12.2

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB oa_data

ADD ./OA/doc/deploy/pg.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
