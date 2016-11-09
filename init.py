#!bin/python
# -*- coding: utf-8 -*-

import os
import json
import argparse
import string
import random
from jinja2 import Template


default_csp = """default-src 'self'; img-src 'self' data: *; style-src 'self' 'unsafe-inline' *.googleapis.com; font-src 'self' data: *.googleapis.com *.gstatic.com; script-src 'self' 'unsafe-inline' 'unsafe-eval' *.googleapis.com; child-src 'self' *.youtube.com; connect-src 'self'; media-src 'self' blob:"""


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

try:
    with open(".config", "r") as in_file:
        defaults = json.load(in_file)
except:
    defaults = {}

parser = argparse.ArgumentParser(description='Docker lemp stack configurator.')
parser.add_argument('-hn', '--hostname', help='Host name', default=defaults.get("hostname", "example.com"), required=False)
parser.add_argument('-p', '--port', help='Http internal nginx port number publically visible', default=defaults.get("port", "7080"), required=False)
parser.add_argument('-cp', '--certificatespath', help='Use this parameter for certificates path', default=defaults.get("certificatespath", False), required=False)
parser.add_argument('-csp', '--contentsecuritypolicy', help='Use this parameter for the value of the content security policy http header',  default=defaults.get("contentsecuritypolicy", default_csp), required=False)
parser.add_argument('-dbn', '--dbname', help='Database name', required=False, default=defaults.get("dbname", "database"))
parser.add_argument('-dbu', '--dbuser', help='Database user', required=False, default=defaults.get("dbuser", "user"))
parser.add_argument('-dbp', '--dbpassword', help='Database password', required=False, default=defaults.get("dbpassword", get_random_string()))
parser.add_argument('-dbrp', '--dbrootpassword', help='Database root password', required=False, default=defaults.get("dbrootpassword", get_random_string()))
parser.add_argument('-rw', '--rewrite', help="Use this parameter if your website uses url rewrite", default=defaults.get("rewrite", False), action='store_true')
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
print ("http port: %s" % args.port)
print ("Database name: %s" % args.dbname)
print ("Database user: %s" % args.dbuser)
print ("Database password: %s" % args.dbpassword)
print ("Database root password: %s" % args.dbrootpassword)
print ("Rewrite is %s" % (args.rewrite and "active" or "not acrive", ))
if args.certificatespath:
    print ("Certificate path is %s" % (args.certificatespath, ))

## save values ##
with open(".config", "w") as out_file:
    json.dump(args_dict, out_file, sort_keys=True, indent=4, separators=(",", ": "))
