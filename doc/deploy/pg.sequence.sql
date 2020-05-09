CREATE SEQUENCE sys_login_id_seq START 1;
CREATE SEQUENCE sys_role_id_seq START 1;
CREATE SEQUENCE sys_function_id_seq START 1;
CREATE SEQUENCE sys_person_id_seq START 1;

alter table "public"."sys_login" alter column "login_id" set default nextval('sys_login_id_seq');
alter table "public"."sys_role" alter column "role_id" set default nextval('sys_role_id_seq');
alter table "public"."sys_function" alter column "function_id" set default nextval('sys_function_id_seq');
alter table "public"."sys_person" alter column "person_id" set default nextval('sys_person_id_seq');