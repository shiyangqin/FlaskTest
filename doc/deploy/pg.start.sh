#!/bin/sh
psql -U postgres -c "CREATE DATABASE oa_data;"
psql -U postgres -d oa_data -c "\i /opt/pg.oa_data.sql"
/bin/bash
