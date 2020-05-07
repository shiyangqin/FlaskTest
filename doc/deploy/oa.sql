--
-- ER/Studio 8.0 SQL Code Generation
-- Company :      Qinsy
-- Project :      Model.DM1
-- Author :       Qinsy
--
-- Date Created : Thursday, May 07, 2020 18:27:20
-- Target DBMS : MySQL 5.x
--

-- 
-- TABLE: sys_function 
--

CREATE TABLE sys_function(
    function_id      INT            NOT NULL,
    function_name    VARCHAR(32),
    cn_name          VARCHAR(32),
    r_person         VARCHAR(64),
    r_time           TIMESTAMP,
    PRIMARY KEY (function_id)
)ENGINE=MYISAM
;



-- 
-- TABLE: sys_login 
--

CREATE TABLE sys_login(
    login_id         INT            NOT NULL,
    user_name        VARCHAR(32),
    user_password    VARCHAR(64),
    login_time       TIMESTAMP      DEFAULT now() NOT NULL,
    repeat           INT            DEFAULT 0 NOT NULL,
    state            CHAR(1)        DEFAULT '1' NOT NULL,
    PRIMARY KEY (login_id)
)ENGINE=MYISAM
;



-- 
-- TABLE: sys_login_role 
--

CREATE TABLE sys_login_role(
    login_id    INT    NOT NULL,
    role_id     INT    NOT NULL,
    PRIMARY KEY (login_id, role_id)
)ENGINE=MYISAM
;



-- 
-- TABLE: sys_person 
--

CREATE TABLE sys_person(
    person_id        INT             NOT NULL,
    login_id         INT             NOT NULL,
    person_name      VARCHAR(32),
    sex              CHAR(1),
    birthday         TIMESTAMP,
    email            VARCHAR(128),
    mobile_phone     BIGINT,
    remark           TEXT,
    state            CHAR(1)         DEFAULT '1' NOT NULL,
    update_person    VARCHAR(64),
    update_time      TIMESTAMP,
    r_person         VARCHAR(64),
    r_time           TIMESTAMP       DEFAULT now(),
    PRIMARY KEY (person_id)
)ENGINE=MYISAM
;



-- 
-- TABLE: sys_role 
--

CREATE TABLE sys_role(
    role_id      INT            NOT NULL,
    role_name    VARCHAR(64),
    r_person     VARCHAR(64),
    r_time       TIMESTAMP      DEFAULT now(),
    PRIMARY KEY (role_id)
)ENGINE=MYISAM
;



-- 
-- TABLE: sys_role_function 
--

CREATE TABLE sys_role_function(
    function_id    INT    NOT NULL,
    role_id        INT    NOT NULL,
    PRIMARY KEY (function_id, role_id)
)ENGINE=MYISAM
;



-- 
-- TABLE: sys_session 
--

CREATE TABLE sys_session(
    token        TEXT           NOT NULL,
    user_info    TEXT,
    user_name    VARCHAR(20),
    ip           VARCHAR(32),
    r_time       TIMESTAMP      DEFAULT now(),
    PRIMARY KEY (token)
)ENGINE=MYISAM
;



-- 
-- TABLE: sys_login_role 
--

ALTER TABLE sys_login_role ADD CONSTRAINT Refsys_login7 
    FOREIGN KEY (login_id)
    REFERENCES sys_login(login_id)
;

ALTER TABLE sys_login_role ADD CONSTRAINT Refsys_role8 
    FOREIGN KEY (role_id)
    REFERENCES sys_role(role_id)
;


-- 
-- TABLE: sys_person 
--

ALTER TABLE sys_person ADD CONSTRAINT Refsys_login6 
    FOREIGN KEY (login_id)
    REFERENCES sys_login(login_id)
;


-- 
-- TABLE: sys_role_function 
--

ALTER TABLE sys_role_function ADD CONSTRAINT Refsys_role9 
    FOREIGN KEY (role_id)
    REFERENCES sys_role(role_id)
;

ALTER TABLE sys_role_function ADD CONSTRAINT Refsys_function10 
    FOREIGN KEY (function_id)
    REFERENCES sys_function(function_id)
;


