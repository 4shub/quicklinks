import webbrowser
import sys
import os
import os.path
import api


# define constants
default_file_name = api.get_file_name()

# define errors
class QuicklinksException(Exception):
    """Base exception for this module"""

def check_for_invalid_index(argIndex, errMessage = ''):
    if len(sys.argv) <= argIndex:
        if errMessage:
            print(errMessage)
        else:
            print('You are missing an argument')

        exit(0)

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

    if operation == '--start-server':
        if len(sys.argv) > 2 and sys.argv[2] == 'debug':
            api.start_server_debug()
        else:
            api.start_server()
        exit(0)

    if operation == '--stop-server':
        api.kill_server()
        exit(0)

    if operation == '--set':
        append_err_msg = 'You need to provide two values when using --set, the key and value \n example: ql --set google https://google.com'
        check_for_invalid_index(2, append_err_msg)
        check_for_invalid_index(3, append_err_msg)

        key = sys.argv[2]
        domain = sys.argv[3]

        api.append_or_update_quicklink(key, domain)
        exit(0)

    if operation == '--remove':
        append_err_msg = 'You need to provide one value when using --remove, the key to what you want to delete \n example: ql --remove google'
        check_for_invalid_index(2, append_err_msg)

        key = sys.argv[2]

        api.remove_quicklink(key)
        exit(0)

    if operation == '--list':
        api.list_quicklinks()
        exit(0)

    if operation == '--help':
        api.list_help()
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