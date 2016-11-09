Brief guide
===========

Requirements:
-------------

Install virtualenv:
virtualenv .
pip install jinja2

Commands to compile docker and config file tempaltes:
-----------------------------------------------------

./init.py -hn example.com -dbn dbname -dbu dbuser -p 6080 -ps 6443
./init.py --help for all the possible values

Command to link nginx:
----------------------

ln -s $PWD/nginx.external.conf /etc/nginx/sites-available/example.com.conf
ln -s /etc/nginx/sites-available/example.com.conf /etc/nginx/sites-enabled/
service nginx testconfig
service nginx reload

Comamnd to build and run docker conainers:
------------------------------------------

docker-compose up -d

Fix permissions
---------------

sudo docker run --rm php:custom-fpm id www-data

will return you a uid and gid (i.e. 33)

chown 33:33 www/ -R
