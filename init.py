#!bin/python
import os
import argparse
import string
import random
from jinja2 import Template


def get_random_string(size=32, chars=string.letters + string.digits + ",;.:-_()="):
    return ''.join(random.choice(chars) for _ in range(size))


def replace_words_in_file(file, values):
    input_file_path = file + ".template"
    input_text = ""
    with open(input_file_path, "r") as input_file:
        input_text = input_file.read()
    input_template = Template(input_text)
    output_text = input_template.render(**values)
    with open(file, "w") as output_file:
        output_file.write(output_text)

parser = argparse.ArgumentParser(description='Docker lemp stack configurator.')
parser.add_argument('-hn', '--hostname', help='Host name', required=True)
parser.add_argument('-pi', '--httpinternalport', help='Http internal nginx port number', default="8080", required=False)
parser.add_argument('-pe', '--httpexternalport', help='Http external ninx port number', default="80", required=False)
parser.add_argument('-cp', '--certificatespath', help='Use this parameter for certificates path', default=False, required=False)
parser.add_argument('-dbn', '--dbname', help='Database name', required=False, default="database")
parser.add_argument('-dbu', '--dbuser', help='Database user', required=False, default="user")
parser.add_argument('-dbp', '--dbpassword', help='Database password', required=False, default=get_random_string())
parser.add_argument('-dbrp', '--dbrootpassword', help='Database root password', required=False, default=get_random_string())
parser.add_argument('-rw', '--rewrite', help="Use this parameter if your website uses url rewrite", default=False, action='store_true')
args = parser.parse_args()
args_dict = vars(args)
 
base_path = os.path.dirname(os.path.realpath(__file__))
nginx_available = "/" + os.path.join("etc", "nginx", "available", args.hostname + ".conf")
nginx_enabled = "/" + os.path.join("etc", "nginx", "enabled", args.hostname + ".conf")
for file in ["docker-compose.yml", "nginx.external.conf", "nginx.internal.conf"]:
    file_path = os.path.join(base_path, file)
    replace_words_in_file(file_path, args_dict)

# TODO: ln -s $PWD/nginx.external.conf /etc/nginx/sites-available/ballardinivini.conf
# TODO: ln -s /etc/nginx/sites-available/ballardinivini.conf /etc/nginx/sites-enabled/ballardinivini.conf

## show values ##
print ("Generated configuration with:")
print ("Host name: %s" % args.hostname)
print ("http ports: %s:%s" % (args.httpinternalport, args.httpexternalport, ))
print ("Database name: %s" % args.dbname)
print ("Database user: %s" % args.dbuser)
print ("Database password: %s" % args.dbpassword)
print ("Database root password: %s" % args.dbrootpassword)
print ("Rewrite is %s" % (args.rewrite and "active" or "not acrive", ))
if args.certificatespath:
    print ("Certificate path is %s" % (args.certificatespath, ))
