--
-- ER/Studio 8.0 SQL Code Generation
-- Company :      Qinsy
-- Project :      Model.DM1
-- Author :       Qinsy
--
-- Date Created : Friday, May 08, 2020 11:59:05
-- Target DBMS : PostgreSQL 8.0
--

-- 
-- TABLE: sys_function 
--

CREATE TABLE sys_function(
    function_id      integer        NOT NULL,
    function_name    varchar(32),
    cn_name          varchar(32),
    r_person         varchar(64),
    r_time           timestamp,
    CONSTRAINT "PK10_1" PRIMARY KEY (function_id)
)
;



-- 
-- TABLE: sys_login 
--

CREATE TABLE sys_login(
    login_id         integer        NOT NULL,
    user_name        varchar(32),
    user_password    varchar(64),
    login_time       timestamp      DEFAULT now() NOT NULL,
    repeat           int4           DEFAULT 0 NOT NULL,
    state            char(1)        DEFAULT '1' NOT NULL,
    CONSTRAINT "PK2_1" PRIMARY KEY (login_id)
)
;



-- 
-- TABLE: sys_login_role 
--

CREATE TABLE sys_login_role(
    login_id    int4    NOT NULL,
    role_id     int4    NOT NULL,
    CONSTRAINT "PK12" PRIMARY KEY (login_id, role_id)
)
;



-- 
-- TABLE: sys_person 
--

CREATE TABLE sys_person(
    person_id        integer         NOT NULL,
    login_id         int4            NOT NULL,
    person_name      varchar(32),
    sex              char(1),
    birthday         timestamp,
    email            varchar(128),
    mobile_phone     int8,
    remark           text,
    state            char(1)         DEFAULT '1' NOT NULL,
    update_person    varchar(64),
    update_time      timestamp,
    r_person         varchar(64),
    r_time           timestamp       DEFAULT now(),
    CONSTRAINT "PK1_1" PRIMARY KEY (person_id)
)
;



-- 
-- TABLE: sys_role 
--

CREATE TABLE sys_role(
    role_id      integer        NOT NULL,
    role_name    varchar(64),
    r_person     varchar(64),
    r_time       timestamp      DEFAULT now(),
    CONSTRAINT "PK88" PRIMARY KEY (role_id)
)
;



-- 
-- TABLE: sys_role_function 
--

CREATE TABLE sys_role_function(
    function_id    int4    NOT NULL,
    role_id        int4    NOT NULL,
    CONSTRAINT "PK95_1" PRIMARY KEY (function_id, role_id)
)
;



-- 
-- TABLE: sys_session 
--

CREATE TABLE sys_session(
    token        text           NOT NULL,
    user_info    text,
    user_name    varchar(20),
    ip           varchar(32),
    r_time       timestamp      DEFAULT now(),
    CONSTRAINT "PK1" PRIMARY KEY (token)
)
;



-- 
-- TABLE: sys_login_role 
--

ALTER TABLE sys_login_role ADD CONSTRAINT "Refsys_login7" 
    FOREIGN KEY (login_id)
    REFERENCES sys_login(login_id)
;

ALTER TABLE sys_login_role ADD CONSTRAINT "Refsys_role8" 
    FOREIGN KEY (role_id)
    REFERENCES sys_role(role_id)
;


-- 
-- TABLE: sys_person 
--

ALTER TABLE sys_person ADD CONSTRAINT "Refsys_login6" 
    FOREIGN KEY (login_id)
    REFERENCES sys_login(login_id)
;


-- 
-- TABLE: sys_role_function 
--

ALTER TABLE sys_role_function ADD CONSTRAINT "Refsys_role9" 
    FOREIGN KEY (role_id)
    REFERENCES sys_role(role_id)
;

ALTER TABLE sys_role_function ADD CONSTRAINT "Refsys_function10" 
    FOREIGN KEY (function_id)
    REFERENCES sys_function(function_id)
;


