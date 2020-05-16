/*
 Navicat Premium Data Transfer

 Source Server         : 10.255.175.224
 Source Server Type    : PostgreSQL
 Source Server Version : 120002
 Source Host           : 10.255.175.224:5432
 Source Catalog        : oa_data
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 120002
 File Encoding         : 65001

 Date: 16/05/2020 17:25:42
*/


-- ----------------------------
-- Sequence structure for sys_user_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."sys_user_id_seq";
CREATE SEQUENCE "public"."sys_user_id_seq" 
INCREMENT 1
MAXVALUE 9223372036854775807
CACHE 1;

-- ----------------------------
-- Table structure for sys_function
-- ----------------------------
DROP TABLE IF EXISTS "public"."sys_function";
CREATE TABLE "public"."sys_function" (
  "function_id" int4 NOT NULL,
  "function_name" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "remark" varchar(64) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of sys_function
-- ----------------------------
INSERT INTO "public"."sys_function" VALUES (1, 'auth', '账户权限');

-- ----------------------------
-- Table structure for sys_person
-- ----------------------------
DROP TABLE IF EXISTS "public"."sys_person";
CREATE TABLE "public"."sys_person" (
  "user_id" int4 NOT NULL,
  "name" varchar(32) COLLATE "pg_catalog"."default",
  "sex" char(1) COLLATE "pg_catalog"."default",
  "birthday" timestamp(6),
  "email" varchar(128) COLLATE "pg_catalog"."default",
  "phone" int8,
  "remark" text COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of sys_person
-- ----------------------------

-- ----------------------------
-- Table structure for sys_role
-- ----------------------------
DROP TABLE IF EXISTS "public"."sys_role";
CREATE TABLE "public"."sys_role" (
  "role_id" int4 NOT NULL,
  "role_name" varchar(64) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Records of sys_role
-- ----------------------------
INSERT INTO "public"."sys_role" VALUES (1, '超级管理员');
INSERT INTO "public"."sys_role" VALUES (2, '管理员');
INSERT INTO "public"."sys_role" VALUES (3, '普通用户');

-- ----------------------------
-- Table structure for sys_role_function
-- ----------------------------
DROP TABLE IF EXISTS "public"."sys_role_function";
CREATE TABLE "public"."sys_role_function" (
  "role_id" int4 NOT NULL,
  "function_id" int4 NOT NULL
)
;

-- ----------------------------
-- Records of sys_role_function
-- ----------------------------
INSERT INTO "public"."sys_role_function" VALUES (1, 1);
INSERT INTO "public"."sys_role_function" VALUES (2, 1);
INSERT INTO "public"."sys_role_function" VALUES (3, 1);

-- ----------------------------
-- Table structure for sys_user
-- ----------------------------
DROP TABLE IF EXISTS "public"."sys_user";
CREATE TABLE "public"."sys_user" (
  "user_id" int4 NOT NULL DEFAULT nextval('sys_user_id_seq'::regclass),
  "user_name" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "user_password" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "login_time" timestamp(6) NOT NULL DEFAULT now(),
  "repeat" int4 NOT NULL DEFAULT 0,
  "state" char(1) COLLATE "pg_catalog"."default" NOT NULL DEFAULT '1'::bpchar,
  "register_time" timestamp(6) NOT NULL DEFAULT now()
)
;

-- ----------------------------
-- Records of sys_user
-- ----------------------------

-- ----------------------------
-- Table structure for sys_user_role
-- ----------------------------
DROP TABLE IF EXISTS "public"."sys_user_role";
CREATE TABLE "public"."sys_user_role" (
  "user_id" int4 NOT NULL,
  "role_id" int4 NOT NULL
)
;

-- ----------------------------
-- Records of sys_user_role
-- ----------------------------

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table sys_function
-- ----------------------------
ALTER TABLE "public"."sys_function" ADD CONSTRAINT "PK10_1" PRIMARY KEY ("function_id");

-- ----------------------------
-- Primary Key structure for table sys_person
-- ----------------------------
ALTER TABLE "public"."sys_person" ADD CONSTRAINT "PK1_1" PRIMARY KEY ("user_id");

-- ----------------------------
-- Primary Key structure for table sys_role
-- ----------------------------
ALTER TABLE "public"."sys_role" ADD CONSTRAINT "PK88" PRIMARY KEY ("role_id");

-- ----------------------------
-- Primary Key structure for table sys_role_function
-- ----------------------------
ALTER TABLE "public"."sys_role_function" ADD CONSTRAINT "PK95_1" PRIMARY KEY ("role_id", "function_id");

-- ----------------------------
-- Primary Key structure for table sys_user
-- ----------------------------
ALTER TABLE "public"."sys_user" ADD CONSTRAINT "PK2_1" PRIMARY KEY ("user_id");

-- ----------------------------
-- Primary Key structure for table sys_user_role
-- ----------------------------
ALTER TABLE "public"."sys_user_role" ADD CONSTRAINT "PK12" PRIMARY KEY ("user_id", "role_id");

-- ----------------------------
-- Foreign Keys structure for table sys_person
-- ----------------------------
ALTER TABLE "public"."sys_person" ADD CONSTRAINT "Refsys_user11" FOREIGN KEY ("user_id") REFERENCES "public"."sys_user" ("user_id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table sys_role_function
-- ----------------------------
ALTER TABLE "public"."sys_role_function" ADD CONSTRAINT "Refsys_function10" FOREIGN KEY ("function_id") REFERENCES "public"."sys_function" ("function_id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."sys_role_function" ADD CONSTRAINT "Refsys_role9" FOREIGN KEY ("role_id") REFERENCES "public"."sys_role" ("role_id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table sys_user_role
-- ----------------------------
ALTER TABLE "public"."sys_user_role" ADD CONSTRAINT "Refsys_role8" FOREIGN KEY ("role_id") REFERENCES "public"."sys_role" ("role_id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."sys_user_role" ADD CONSTRAINT "Refsys_user7" FOREIGN KEY ("user_id") REFERENCES "public"."sys_user" ("user_id") ON DELETE NO ACTION ON UPDATE NO ACTION;
