from platform import system, release
import PythonRegistryDiffer.userfunctions as exec
from PythonRegistryDiffer.database import Database

header = """
Python Registry Differ version xA
Type 'help' for help.
"""


def process_general_commands(cmd):
    cmd = cmd.lower().split(' ')
    if cmd[0] == 'help':
        prd_help_closed()
    elif cmd[0] == 'new-db':
        new_db(cmd)
    elif cmd[0] == 'load-db':
        load_db(cmd)
    elif cmd[0] == 'exit':
        return False
    return True


def process_database_commands(cmd, db):
    print('not implemented')
    return False


def load_db(args):
    if len(args) != 3 or args[1] != '-f':
        print("Invalid arguments to load a DB: \n{}\nType 'help' for help.".format(args))
    open_db(args[2])


def new_db(args):
    if len(args) <= 1:
        print('Not enough arguments.')
        return
    filename = ''
    hklm = True
    hkcu = True
    hku = True
    hkcc = True
    hkcr = True

    args.remove('new-db')

    if '-f' in args and '-m' not in args:
        filename = args[args.index('-f')+1]
        if filename in ('--no-hklm',
                        '--no-hkcu',
                        '--no-hku',
                        '--no-hkcc',
                        '--no-hkcr') or len(args) <= 1:  # make sure there's still enough arguments after drops
            print('-f was used but no file name was input')
            return
        args.remove(args[args.index('-f')+1])
        args.remove('-f')
    elif '-m' in args and '-f' not in args:
        filename = 'memory'
        args.remove('-m')
    else:
        print("Invalid arguments to create a new database: \n{}\nType 'help' for help.".format(args))

    if '--no-hklm' in args:
        hklm = False
        args.remove('--no-hklm')
    if '--no-hkcu' in args:
        hkcu = False
        args.remove('--no-hkcu')
    if '--no-hku' in args:
        hku = False
        args.remove('--no-hku')
    if '--no-hkcc' in args:
        hkcc = False
        args.remove('--no-hkcc')
    if '--no-hkcr' in args:
        hkcr = False
        args.remove('--no-hkcr')

    if len(args) is not 0:
        print('Unknown arguments: {}'.format(args))
    open_db(filename, hklm, hkcu, hku, hkcr, hkcc)


def open_db(location, hklm=True, hkcu=True, hku=True, hkcr=True, hkcc=True):
    # open the DB
    # call the process inner commands function with the db object
    dbo = Database(location, True, hklm, hkcu, hku, hkcr, hkcc)

    with dbo as db:
        while True:
            cmd = input('> ').lower().split(' ')
            if process_database_commands(cmd, db):
                continue
            else:
                break


def main():
    print(header)

    db = None
    while True:
        cmd = input('> ')
        if process_general_commands(cmd):
            continue
        else:
            break


if __name__ == '__main__':
    if 'windows' not in system().lower():
        print('This program must be run on a Windows host. Detected \'{} {}\'. Quitting...'.format(system(), release()))
    else:
        main()


def prd_help_closed():
    print("""Commands in current context:

        new-db      : Creates a new database to host images of the registry. Requires the use of -f or -m.

        load-db     : Loads an existing baseline (and any previously saved comparison images) from the specified file.
                      *-f filename
                      *Not using -f will reload the current db's save file without saving any changes made in the
                      current session.

        help        : Show this help information

OPTIONS:

        -f | --file <filename> : The database or report file to use/save as/load from
                      IE:
                      "load-db -f C:\Work\Registry_set.db"
                      "diff-images 1 2 -f registry-report.txt" 

        <only for use with the 'new-db' command>
        --no-hklm : Exclude the HKEY_LOCAL_MACHINE root key.
           *hkcc : Exclude the HKEY_CURRENT_CONFIG root key.
           *hkcr : Exclude the HKEY_CLASSES_ROOT root key.
           *hku  : Exclude the HKEY_USER root key.
           *hkcu : Exclude the HKEY_CURRENT_USER root key.

        -m | --memorymode   : Keeps the database in memory mode instead of saving it.
""")


def prd_help_open():
    print("""Commands in current context:
        new-image   : Creates a new comparison image. It will only check the HKEYs that the database was created with.
                      Requires a machine ID.
                      "new-image machine=1"

        list-images : Lists the number of current images in the db and some cursory details.

        diff-images : Generates a report that compares two different registry images. Enter the image numbers from 
                     list-images as arguments to designate which images to compare. Use "-f filename" to save the report
                     to a file. Examples:
                    "diff-images 0 3" 
                    "diff-images 2 0"
                    "diff-images 1 2 -f registry-report.txt" 

        close-db    : Close this database and prepare to create/load another. Databases in memory will be destroyed.

        add-machine : Adds a new machine to this database. If given both, the hostname will always be used to connect.
                    Must have either an IP or a hostname:
                    "add-machine ip=127.0.0.1"
                    "add-machine hostname=localhost"
                    "add-machine ip=192.168.0.2 hostname=mywinserver01"

        list-machines : Prints a list of machines in this database.

        update-machine : Similar to add machine; except it updates the specified fields. Use the machine ID to specify
                         which machine to edit.
                         "update-machine
        -h | help   : Show this help information


        -f | --file <filename> : The database or report file to use/save as/load from
              IE:
              "load-db -f C:\Work\Registry_set.db"
              "diff-images 1 2 -f registry-report.txt" 
""")
