#!bin/python
# -*- coding: utf-8 -*-

from crontab import CronTab
from jinja2 import Template

import argparse
import errno
import json
import logging
import os
import random
import stat
import string


logging.basicConfig()
logger = logging.getLogger(__name__)


default_csp = ("default-src 'self'; img-src 'self' data: *; style-src 'self' "
               "'unsafe-inline' *.googleapis.com; font-src 'self' data: "
               "*.googleapis.com *.gstatic.com; script-src 'self' "
               "'unsafe-inline' 'unsafe-eval' *.googleapis.com; child-src "
               "'self' *.youtube.com; connect-src 'self'; media-src 'self'")

password_chars = string.letters + string.digits + ",;.:-_()="


def get_random_string(size=32, chars=password_chars):
    return ''.join(random.choice(chars) for _ in range(size))


def replace_words_in_file(base_path, file, values):
    src_file = file + ".jinja2"
    src_file_path = os.path.join(base_path, "config.jinja2", src_file)
    dst_file_path = os.path.join(base_path, "config", file)
    input_text = ""
    with open(src_file_path, "r") as src_file:
        input_text = src_file.read()
    input_template = Template(input_text)
    output_text = input_template.render(**values)
    with open(dst_file_path, "w") as output_file:
        output_file.write(output_text)
    return dst_file_path


def create_link_if_not_exist(source, dest):
    try:
        os.symlink(source, dest)
    except Exception as e:
        if e.errno == errno.EEXIST:
            logger.info("Cannot create link because file '%s' already exists",
                        dest)
        logger.warning("Could not create symlink: from %s to %s with error %s",
                       source, dest, e)


def create_nginx_links(file, hostname):
    nginx_available = "/" + os.path.join("etc", "nginx", "sites-available",
                                         hostname + ".conf")
    nginx_enabled = "/" + os.path.join("etc", "nginx", "sites-enabled",
                                       hostname + ".conf")
    create_link_if_not_exist(file, nginx_available)
    create_link_if_not_exist(nginx_available, nginx_enabled)


try:
    with open(".config", "r") as in_file:
        defaults = json.load(in_file)
except:
    defaults = {}

parser = argparse.ArgumentParser(description='Docker lemp stack configurator.')
parser.add_argument('-hn', '--hostname', help='Host name',
                    default=defaults.get("hostname", "example.com"),
                    required=False)
parser.add_argument('-p', '--port',
                    help='Http internal nginx port number publically visible',
                    default=defaults.get("port", "7080"), required=False)
parser.add_argument('-cp', '--certificatespath',
                    help='Use this parameter for certificates path',
                    default=defaults.get("certificatespath", False),
                    required=False)
parser.add_argument('-csp', '--contentsecuritypolicy',
                    help='Use this parameter for the value of the content '
                    'security policy http header',
                    default=defaults.get("contentsecuritypolicy", default_csp),
                    required=False)
parser.add_argument('-pn', '--projectname', help='Name of the project',
                    required=False, default=defaults.get("projectname",
                                                         "project"))
parser.add_argument('-dbn', '--dbname', help='Database name', required=False,
                    default=defaults.get("dbname", "database"))
parser.add_argument('-dbu', '--dbuser', help='Database user', required=False,
                    default=defaults.get("dbuser", "user"))
parser.add_argument('-dbp', '--dbpassword', help='Database password',
                    required=False,
                    default=defaults.get("dbpassword", get_random_string()))
parser.add_argument('-dbrp', '--dbrootpassword', help='Database root password',
                    required=False, default=defaults.get("dbrootpassword",
                                                         get_random_string()))
parser.add_argument('-pv', '--phpversion', help='php version: 5 or 7',
                    required=False, default=defaults.get("phpversion", '7'))
parser.add_argument('-pul', '--phpuploadlimit', help='max MB uplodable',
                    required=False, default=defaults.get("phpuploadlimit", '2'))
parser.add_argument('-rw', '--rewrite',
                    help="Use this parameter if your website uses url rewrite",
                    default=defaults.get("rewrite", False),
                    action='store_true')
parser.add_argument('-v', '--verbose',
                    help="Use this parameter to see verbose output",
                    default=defaults.get("verbose", False),
                    action='store_true')
args = parser.parse_args()
args_dict = vars(args)
if args.verbose:
    logger.setLevel(logging.DEBUG)

base_path = os.path.dirname(os.path.realpath(__file__))
root_cron = None
try:
    root_cron = CronTab(user='root')
except IOError:
    logger.warning("Not changing cronjob: not root")
for file in ["docker-compose.yml",
             "nginx.external.conf",
             "nginx.internal.conf",
             "php.dockerfile",
             "php.override.ini",
             "cron-backup.sh", ]:
    file_path = replace_words_in_file(base_path, file, args_dict)
    if file == "nginx.external.conf":
        create_nginx_links(file_path, args.hostname)
    if file.endswith(".sh"):
        st = os.stat(file_path)
        os.chmod(file_path, st.st_mode | stat.S_IEXEC)

    if file.startswith("cron-"):
        if root_cron:
            old_jobs = root_cron.find_command(file_path)
            for job in old_jobs:
                root_cron.remove(job)

            root_job = root_cron.new(command=file_path)
            root_job.minute.on(30)
            root_job.hour.on(2)
            root_job.enable()
            root_cron.write()

# save values #
with open(".config", "w") as out_file:
    json.dump(args_dict, out_file, sort_keys=True, indent=4)
