#!/bin/bash
psql -U postgres -c "CREATE DATABASE oa_data;"
psql -U postgres -d oa_data -c "\i /opt/pg.sql"