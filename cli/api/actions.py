from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
from pathlib import Path

import os
import re

# define constants
default_file_name = os.path.join(str(Path.home()), '.quicklinks')

def get_file_name():
    return default_file_name

# Taken from django
# https://github.com/django/django/blob/master/django/core/validators.py
is_website_regex = re.compile(
    r'^(?:http|file)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def check_if_valid_domain(domain):
    if re.match(is_website_regex, domain) is None:
        print('You have not provided a valid domain, for now please add http:// or https:// to the start of domains')
        exit(0)


def append_or_update_quicklink(key, domain):
    check_if_valid_domain(domain)

    updated = False

    fh, abs_path = mkstemp()

    str_to_write = '%s:%s' % (key, domain)

    with fdopen(fh, 'w') as new_file, open(default_file_name) as old_file:
        for line in old_file:
            line = line.strip()

            if not line:
                continue

            if line.split(':', 1)[0] == key:
                new_file.write(str_to_write)
                updated = True
            else:
                new_file.write(line)

        if not updated:
            new_file.write('\n%s\n' % str_to_write)

    remove(default_file_name)
    move(abs_path, default_file_name)

def remove_quicklink(key):
    fh, abs_path = mkstemp()

    with fdopen(fh, 'w') as new_file, open(default_file_name) as old_file:
        for line in old_file:
            line = line.strip()

            if not line:
                continue

            if not (line.split(':', 1)[0] == key):
                new_file.write(line)

    remove(default_file_name)
    move(abs_path, default_file_name)

def list_quicklinks():
    with open(default_file_name) as file:
        for line in file:
            print(line.strip())

def list_help():
    help_text = '''Standard quicklinks usage:
ql <key> 

Helper commands:
    --set: allows you to set a new quick link
        usage: ql --set <key> <url>
    --remove: allows you to remove a quick link
        usage: ql --remove <key>
    --list: lists all your current quick links
        usage: ql --list
    '''

    print(help_text)