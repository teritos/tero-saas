Help me with Docker:
====================

Create Tero DB:
---------------

@math:docker(devel**) $ docker exec -it docker_pgsql_1 psql -U postgres
psql (9.5.4)
Type "help" for help.

postgres=# \db
       List of tablespaces
    Name    |  Owner   | Location 
------------+----------+----------
 pg_default | postgres | 
 pg_global  | postgres | 
(2 rows)

postgres=# create database tero;
CREATE DATABASE
postgres=# ^D

Then, login into tero container:
@math:docker(devel**) $ docker exec -it docker_tero_1 /bin/bash

Activate virtualenv
root@a9aad69f8d24:/# source /env/bin/activate

Go to /tero and run manage.py migrate:

(env) root@a9aad69f8d24:/tero# ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, alarm, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying alarm.0001_initial... OK
  Applying alarm.0002_auto_20170121_2047... OK
  Applying alarm.0003_backfill_labels... OK
  Applying alarm.0004_device... OK
  Applying alarm.0005_auto_20170603_1918... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying sessions.0001_initial... OK
(env) root@a9aad69f8d24:/tero# 