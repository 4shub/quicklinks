import webbrowser
import sys
import os
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
import re
from pathlib import Path
import os.path

# define errors
class QuicklinksException(Exception):
    """Base exception for this module"""


class QuicklinksCLIError(QuicklinksException):
    """Generic exception for raising errors during CLI operation"""

class QucklinksInvalidQuickLinksDotFile(QuicklinksException):
    """Dotfile is misconfigured, please fix at ~/.quicklinks"""

# define constants
default_file_name = os.path.join(str(Path.home()), '.quicklinks')

# Taken from django
# https://github.com/django/django/blob/master/django/core/validators.py
is_website_regex = re.compile(
    r'^(?:http|file)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def check_for_invalid_index(argIndex, errMessage = ''):
    if len(sys.argv) <= argIndex:
        if errMessage:
            print(errMessage)
        else:
            print('You are missing an argument')

        exit(0)

def check_if_valid_domain(domain):
    if re.match(is_website_regex, domain) is None:
        print('You have not provided a valid domain, for now please add http:// or https:// to the start of domains')
        exit(0)


def append_or_update_quicklink():
    append_err_msg = 'You need to provide two values when using --set, the key and value \n example: ql --set google https://google.com'
    check_for_invalid_index(2, append_err_msg)
    check_for_invalid_index(3, append_err_msg)

    key = sys.argv[2]
    domain = sys.argv[3]

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

def remove_quicklink():
    append_err_msg = 'You need to provide one value when using --remove, the key to what you want to delete \n example: ql --remove google'
    check_for_invalid_index(2, append_err_msg)

    key = sys.argv[2]

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

def check_if_quicklinks_file_exists():
    if not os.path.exists(default_file_name):
        print('.quicklinks file does not exist, create one at ~/.quicklinks')
        exit(0)

def operation_handler():
    check_for_invalid_index(1)

    check_if_quicklinks_file_exists()

    operation = sys.argv[1]
    if not operation:
        exit(1)

    if operation == '--set':
        append_or_update_quicklink()
        exit(0)

    if operation == '--remove':
        remove_quicklink()
        exit(0)

    if operation == '--list':
        list_quicklinks()
        exit(0)

    if operation == '--help':
        list_help()
        exit(0)

    open_existing_link()

def search_for_value(search_key, callback):
    with open(default_file_name) as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            try:
                shortcut, domain = line.split(':', 1)
                if shortcut == search_key:
                    callback(shortcut, domain)
            except ValueError:
                raise QuicklinksException('bad')

def open_existing_link():
    def open_link(shortcut, domain):
        webbrowser.open(domain, new=0, autoraise=True)

    search_for_value(sys.argv[1], open_link)

def get_exception():
    """Helper function to work with py2.4-py3 for getting the current
    exception in a try/except block
    """
    return sys.exc_info()[1]

def main():
    try:
        operation_handler()
    except KeyboardInterrupt:
        print('goodbye!')
    except (QuicklinksException, SystemExit):
        e = get_exception()

        # Ignore a successful exit, or argparse exit
        if getattr(e, 'code', 1) not in (0, 2):
            raise SystemExit('ERROR: %s' % e)


if __name__ == '__main__':
    main()