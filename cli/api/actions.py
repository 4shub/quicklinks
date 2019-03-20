from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
from pathlib import Path

import re
import os

# default file path for ~/.quicklinks on computer
default_file_name = os.path.join(str(Path.home()), '.quicklinks')

def get_file_name():
    return default_file_name

def send_permission_error():
    print('\nQuicklinks cannot access this file, please enable group read write access by doing the following:\nsudo chmod 604 ~/.quicklinks\n')
    exit(0)


def append_or_update_quicklink(key, url):
    """
    Adds a quicklink to the ~/.quicklinks file or updates an existing quicklink given a key and url

    :param key: key of quicklink to add/update
    :param url: url of a website to quicklink to
    """

    if not re.match("https?://", url):
        url = 'http://' + url

    updated = False

    fh, abs_path = mkstemp()

    str_to_write = '%s:%s' % (key, url)

    try:
        with fdopen(fh, 'w') as new_file, open(default_file_name) as old_file:
            for line in old_file:
                line = line.strip()

                if not line:
                    continue

                line = line + '\n'

                if line.split(':', 1)[0] == key:
                    new_file.write(str_to_write)
                    updated = True
                else:
                    new_file.write(line)

            if not updated:
                new_file.write('%s\n' % str_to_write)
    except PermissionError:
        send_permission_error()

    remove(default_file_name)
    move(abs_path, default_file_name)

def remove_quicklink(key):
    """
    Removes quicklink from ~/.quicklinks file

    :param key: key of quicklink to delete
    """

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
    """
    Returns a list of QuickLinks
    :return: list<String> list of quick links
    """

    quicklinks_list = []

    with open(default_file_name) as file:
        for line in file:
            quicklinks_list.append(line.strip())

    return quicklinks_list

def search_for_value(search_key, callback):
    """
    Searches for a quicklink in ~/.quicklinks file
    :param search_key: key to search in the quicklinks file
    :param callback: callback to run after finding the search value
    :return:
    """

    succeeded = False

    try:
        with open(default_file_name) as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                try:
                    shortcut, domain = line.split(':', 1)
                    if shortcut == search_key:
                        succeeded = True
                        callback(shortcut, domain)
                except ValueError:
                    raise 'An error has occured'
    except PermissionError:
        send_permission_error()

    return succeeded