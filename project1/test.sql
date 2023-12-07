CREATE DATABASE photoapp;
select now();
USE photoapp;

DROP TABLE IF EXISTS assets;
DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    userid       int not null AUTO_INCREMENT,
    email        varchar(128) not null,
    lastname     varchar(64) not null,
    firstname    varchar(64) not null,
    bucketfolder varchar(48) not null,  -- random, unique name (UUID)
    PRIMARY KEY (userid),
    UNIQUE      (email),
    UNIQUE      (bucketfolder)
);

ALTER TABLE users AUTO_INCREMENT = 80001;  -- starting value

CREATE TABLE assets
(
    assetid      int not null AUTO_INCREMENT,
    userid       int not null,
    assetname    varchar(128) not null,  -- original name from user
    bucketkey    varchar(128) not null,  -- random, unique name in bucket
    PRIMARY KEY (assetid),
    FOREIGN KEY (userid) REFERENCES users(userid),
    UNIQUE      (bucketkey)
);

ALTER TABLE assets AUTO_INCREMENT = 1001;  -- starting value

-- inserts one user and one asset into respective tables:
--
-- NOTE: userid in users table is automatically generated, so we
-- don't provide a userid. Likewise for assetid in assets table.
--

USE photoapp;

INSERT INTO 
  users(email, lastname, firstname, bucketfolder)
  values('andy@northwestern.edu', 'cheng', 'jingze', 
         '59d7c92f-a237-4bd2-9503-145c3f295a29  /');

INSERT INTO 
  assets(userid, assetname, bucketkey)
  values(
         '61cfa37d-b6bc-42f2-ac93-7eacb8e18074',
         '59d7c92f-a237-4bd2-9503-145c3f295a29  /61cfa37d-b6bc-42f2-ac93-7eacb8e18074   ');
  
INSERT INTO
  users(email, lastname, firstname, bucketfolder)
  values('andy@northwestern.edu', 'cheng', 'jingze', 
         '59d7c92f-a237-4bd2-9503-145c3f295a29  /')
  
INSERT INTO 
  assets(userid, assetname, bucketkey)
  values( 
         'bac72c07-a144-4244-8fe5-cbb3c2762462',
         '59d7c92f-a237-4bd2-9503-145c3f295a29  /bac72c07-a144-4244-8fe5-cbb3c2762462  ');
INSERT INTO 
  users(email, lastname, firstname, bucketfolder)
  values('diana@northwestern.edu', 'gong', 'jinwen', 
         '728e822b-14db-453b-8705-d47cfd8beab1  /');
         
INSERT INTO 
  assets(userid, assetname, bucketkey)
  values(
         '9c456bad-cb49-404f-93cf-d3441d17132c',
         '728e822b-14db-453b-8705-d47cfd8beab1  /9c456bad-cb49-404f-93cf-d3441d17132c');
        
INSERT INTO 
  users(email, lastname, firstname, bucketfolder)
  values('diana@northwestern.edu', 'gong', 'jinwen', 
         '728e822b-14db-453b-8705-d47cfd8beab1  /');
         
INSERT INTO 
  assets(userid, assetname, bucketkey)
  values(
         'f3fac5c2-8da9-4d5f-aae3-47d503603389',
         '728e822b-14db-453b-8705-d47cfd8beab1  /f3fac5c2-8da9-4d5f-aae3-47d503603389   ');


INSERT INTO 
  users(email, lastname, firstname, bucketfolder)
  values('eco@northwestern.edu', 'liu', 'zheng', 
         '8ace2246-bbd5-4fc7-848f-3e8aba91032c  /');
         
INSERT INTO 
  assets(userid, assetname, bucketkey)
  values(
         'b777c03d-767e-4036-a4f0-43a5412ad237',
         '8ace2246-bbd5-4fc7-848f-3e8aba91032c  /b777c03d-767e-4036-a4f0-43a5412ad237   ');   
INSERT INTO 
  users(email, lastname, firstname, bucketfolder)
  values('eco@northwestern.edu', 'liu', 'zheng', 
         '8ace2246-bbd5-4fc7-848f-3e8aba91032c  /');
         
INSERT INTO 
  assets(userid, assetname, bucketkey)
  values(
         'db724771-33f4-4673-a751-6dd6926309ad',
         '8ace2246-bbd5-4fc7-848f-3e8aba91032c  /db724771-33f4-4673-a751-6dd6926309ad  '); 
    

USE photoapp;
SELECT * FROM users;

USE photoapp;
SELECT * FROM assets;

USE photoapp;
DROP USER IF EXISTS 'photoapp-read-only';
DROP USER IF EXISTS 'photoapp-read-write';
CREATE USER 'photoapp-read-only' IDENTIFIED BY 'abc123!!';
CREATE USER 'photoapp-read-write' IDENTIFIED BY 'def456!!';
GRANT SELECT, SHOW VIEW ON photoapp.* 
 TO 'photoapp-read-only';
GRANT SELECT, SHOW VIEW, INSERT, UPDATE, DELETE ON photoapp.* 
 TO 'photoapp-read-write';
 
FLUSH PRIVILEGES;

USE photoapp;
SELECT * FROM users;
SELECT * FROM assets;
