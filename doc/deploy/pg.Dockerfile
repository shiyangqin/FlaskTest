FROM postgres:12.2

ADD /opt/OA/doc/deploy/oa.sql /opt/oa.sql

RUN psql -U postgres -c "CREATE DATABASE oa_data;" \
    && psql -U postgres -d oa_data -c "\i /opt/oa.sql"

EXPOSE 5432
