Brief guide
===========

Requirements:
-------------

existing nginx on host machine
docker and docker-compose installed
Install virtualenv:
virtualenv .
pip install -r requirements.txt 

Comamnds to build and run docker conainers:
------------------------------------------

First we have to call the init script that compiles the configuration templates
into real configuration files for docker compose and nginx (both int and ext)

./init.py -hn example.com -p 7080 -rw -dbn db_name -dbu db_user
docker-compose up -d
service nginx reload

The init script help:
--------------------------

Docker lemp stack configurator.

optional arguments:
  -h, --help            show this help message and exit
  -hn HOSTNAME, --hostname HOSTNAME
                        Host name
  -p PORT, --port PORT  Http internal nginx port number publically visible
  -cp CERTIFICATESPATH, --certificatespath CERTIFICATESPATH
                        Use this parameter for certificates path
  -csp CONTENTSECURITYPOLICY, --contentsecuritypolicy CONTENTSECURITYPOLICY
                        Use this parameter for the value of the content
                        security policy http header
  -dbn DBNAME, --dbname DBNAME
                        Database name
  -dbu DBUSER, --dbuser DBUSER
                        Database user
  -dbp DBPASSWORD, --dbpassword DBPASSWORD
                        Database password
  -dbrp DBROOTPASSWORD, --dbrootpassword DBROOTPASSWORD
                        Database root password
  -rw, --rewrite        Use this parameter if your website uses url rewrite
  -v, --verbose         Use this parameter to see verbose output

The configuration params will be printed on screen and saved on a .config file
params order of resultion is:

cli arguments -> .config fie -> defaults

The init script, after compiling the external nginx configuration file will
create a symlink in te appropriated nginx directory:
/etc/nginx/sites-(available|enabled)/example.com.conf

If we want to make everyting this effective we will have to restart nginx:
service nginx reload

Fix permissions
---------------

www directory will have all files created by the user running all the process
above. If your architecture requires write permission (i.e. wordpress plugin
installation via web interface) you will have to change the owner:

sudo docker run --rm php:custom-fpm id www-data

will return you a uid and gid (i.e. 33)

chown 33:33 www/ -R

HTTPS
-----

To use https you can use certificatespath arguemnt writing the path where the
certificates are. The certificates must have been created externally
using certpath command (installed as python requirement)
