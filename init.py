#!/usr/bin/python
import os
import argparse
import string
import random

def get_random_string(size=32, chars=string.letters + string.digits + ",;.:-_()="):
    return ''.join(random.choice(chars) for _ in range(size))

def replace_words_in_file(file, values):
    input_file_path = file + ".template"
    input_text = ""
    with open(input_file_path, "r") as input_file:
        input_text = input_file.read()
    input_template = string.Template(input_text)
    output_text = input_template.substitute(values)
    with open(file, "w") as output_file:
        output_file.write(output_text)

parser = argparse.ArgumentParser(description='Docker lemp stack configurator.')
parser.add_argument('-hn', '--hostname', help='Host name', required=True)
parser.add_argument('-p', '--httpport', help='Http internal port number', default="7080", required=False)
parser.add_argument('-ps', '--httpsport', help='Https internal port number', default="7443", required=False)
parser.add_argument('-dbn', '--dbname', help='Database name', required=False, default="database")
parser.add_argument('-dbu', '--dbuser', help='Database user', required=False, default="user")
parser.add_argument('-dbp', '--dbpassword', help='Database password', required=False, default=get_random_string())
parser.add_argument('-dbrp', '--dbrootpassword', help='Database root password', required=False, default=get_random_string())
args = parser.parse_args()
args_dict = vars(args)
 
base_path = os.path.dirname(os.path.realpath(__file__))
nginx_available = "/" + os.path.join("etc", "nginx", "available", args.hostname + ".conf")
nginx_enabled = "/" + os.path.join("etc", "nginx", "enabled", args.hostname + ".conf")
for file in ["docker-compose.yml", "nginx.external.conf", ]:
    file_path = os.path.join(base_path, file)
    replace_words_in_file(file_path, args_dict)

## show values ##
print ("Generated configuration with:")
print ("Host name: %s" % args.hostname)
print ("http port: %s" % args.httpport)
print ("https port: %s" % args.httpsport)
print ("Database name: %s" % args.dbname)
print ("Database user: %s" % args.dbuser)
print ("Database password: %s" % args.dbpassword)
print ("Database root password: %s" % args.dbrootpassword)
