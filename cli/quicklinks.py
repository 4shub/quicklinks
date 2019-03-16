import webbrowser
import sys
import os
import os.path
import api


# define constants
default_file_name = api.get_file_name()


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

def cli_help_text():
    help_text = '''Standard quicklinks usage:
ql <key> 

Helper commands:
    --set: allows you to set a new quick link
        usage: ql --set <key> <url>
    --remove: allows you to remove a quick link
        usage: ql --remove <key>
    --list: lists all your current quick links
        usage: ql --list
    
Server commands:
    --start-server: Starts Quicklinks Server
        usage: ql --start-server
    --start-server debug: Starts Quicklinks server in debug mode
        usage: ql --start-server debug
    --stop-server: Stops Quicklinks Server
        usage: ql --stop-server
    '''

    print(help_text)



def open_existing_link(search_key):
    """
    Opens a link given particular key

    :param search_key: key to search in the quicklinks file
    :return:
    """
    def open_link(shortcut, domain):
        webbrowser.open(domain, new=0, autoraise=True)

    did_succeed = api.search_for_value(search_key, open_link)

    if not did_succeed:
        raise ValueError('No quicklink found for this key! \nPlease edit your ~/.quicklinks file or use ql --set <key> <url>')

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

    elif operation == '--stop-server':
        api.kill_server()

    elif operation == '--set':
        append_err_msg = 'You need to provide two values when using --set, the key and value \n example: ql --set google https://google.com'
        check_for_invalid_index(2, append_err_msg)
        check_for_invalid_index(3, append_err_msg)

        key = sys.argv[2]
        domain = sys.argv[3]

        api.append_or_update_quicklink(key, domain)

    elif operation == '--remove':
        append_err_msg = 'You need to provide one value when using --remove, the key to what you want to delete \n example: ql --remove google'
        check_for_invalid_index(2, append_err_msg)

        key = sys.argv[2]

        api.remove_quicklink(key)

    elif operation == '--list':
        quicklinks_list = api.list_quicklinks()

        print(quicklinks_list)

    elif operation == '--help':
        cli_help_text()
    else:
        # if there are no special arguments provided then run quicklinks
        key = sys.argv[1]

        open_existing_link(key)

    exit(0)

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
    except (ValueError, SystemExit):
        e = get_exception()

        # Ignore a successful exit, or argparse exit
        if getattr(e, 'code', 1) not in (0, 2):
            raise SystemExit('ERROR: %s' % e)


if __name__ == '__main__':
    main()