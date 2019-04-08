import re
import os
import pathlib
import shutil
import tempfile

# default file path for ~/.quicklinks on computer
DEFAULT_FILE = os.path.join(str(pathlib.Path.home()), '.quicklinks')
PERMISSION_ERROR_STRING = '''
    Quicklinks cannot access this file, please enable group read write
    access by doing the following:
    sudo chmod 604 ~/.quicklinks'''


def append_or_update_quicklink(key, url):
    """
    Adds a quicklink to the ~/.quicklinks file or updates an existing quicklink
    given a key and url.

    :param key: key of quicklink to add/update.
    :param url: url of a website to quicklink.
    """

    if not re.match("https?://", url):
        url = 'http://{}'.format(url)

    updated = False
    fh, abs_path = tempfile.mkstemp()
    str_to_write = '{}:{}'.format(key, url)

    try:
        # TODO: Switch to CSV
        with os.fdopen(fh, 'w') as new_file, open(DEFAULT_FILE) as old_file:
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
        raise PermissionError(PERMISSION_ERROR_STRING)

    os.remove(DEFAULT_FILE)
    shutil.move(abs_path, DEFAULT_FILE)


def remove_quicklink(key):
    """
    Removes quicklink from ~/.quicklinks file

    :param key: key of quicklink to delete
    """

    fh, abs_path = tempfile.mkstemp()
    # TODO: Switch to CSV
    with os.fdopen(fh, 'w') as new_file, open(DEFAULT_FILE) as old_file:
        for line in old_file:
            line = line.strip()

            if not line:
                continue

            if not line.split(':', 1)[0] == key:
                new_file.write(line)

    os.remove(DEFAULT_FILE)
    shutil.move(abs_path, DEFAULT_FILE)


def list_quicklinks():
    """
    Returns a list of QuickLinks
    :return: list<String> list of quick links
    """

    quicklinks_list = []

    with open(DEFAULT_FILE) as file:
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
        # TODO: Switch to CSV
        with open(DEFAULT_FILE) as file:
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
                    print('An error has occurred')
                    raise
    except PermissionError:
        raise PermissionError(PERMISSION_ERROR_STRING)

    return succeeded
