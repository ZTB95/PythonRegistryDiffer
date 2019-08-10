import os.path as path
import PythonRegistryDiffer.userfunctions as prd
from PythonRegistryDiffer.database import Database
from platform import system, release

header = """
Python Registry Differ version xA
Type 'help' for help.
"""

is_windows = bool  # used to prevent attempts at create new databases or registry images on unsupported machines.


# DATABASE SELECTION COMMAND SECTION
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


def load_db(args):
    if len(args) != 3 or args[1] != '-f':
        print("Invalid arguments to load a DB: \n{}\nType 'help' for help.".format(args))
        return
    if path.exists(args[2]):
        open_db(args[2])
    else:
        print('File does not exist. Load failed.')


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
    open_db(filename, hklm, hkcu, hku, hkcr, hkcc, True)


def open_db(location, hklm=True, hkcu=True, hku=True, hkcr=True, hkcc=True):
    # open the DB
    # call the process inner commands function with the db object
    dbo = Database(location, True, hklm, hkcu, hku, hkcr, hkcc)

    with dbo as db:
        while True:
            cmd = input('{}> '.format(db.location[-16:0])).lower().split(' ')
            if process_database_commands(cmd, db):
                continue
            else:
                break


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


def new_image(cmd, db):
    quiet = False
    machine_id = 0

    if len(cmd) not in (1, 2, 3, 4):
        print('Unkown arguments: {}'.format(cmd))
        return
    elif '-q' in cmd or '--quiet' in cmd:  # more verbose than it needs to be, but for clarity's sake
        print('Quiet mode has not been implemented yet for new-image. Continuing anyway...')
        quiet = True  # TODO: Implement quiet mode for new-image command
        if '-q' in cmd:
            cmd.remove('-q')
        elif '--quiet' in cmd:
            cmd.remove('--quiet')
    if '-i' in cmd:
        try:
            machine_id = int(cmd[cmd.index('-i') + 1])
        except:
            print('Bad machine ID: {}'.format(cmd))
            return
         # TODO: Make sure ths machine actually exists. Will likely throw an exception if it doesn't.
    prd.new_image(machine_id, db)


def new_machine(cmd, db):
    pass


def list_images(cmd, db):
    pass


def list_machines(cmd, db):
    pass


def diff_images(cmd, db):
    pass


def update_machine(cmd, db):
    pass


# DATABASE OPENED COMMAND SECTION
def process_database_commands(cmd, db):
    if cmd[0] == 'exit':
        return True
    elif cmd[0] == 'new-image':
        new_image(cmd, db)
    elif cmd[0] == 'new-machine':
        new_machine(cmd, db)
    elif cmd[0] == 'list-images':
        list_images(cmd, db)
    elif cmd[0] == 'list-machines':
        list_machines(cmd, db)
    elif cmd[0] == 'update-machine':
        update_machine(cmd, db)
    elif cmd[0] == 'diff-images':
        diff_images(cmd, db)
    elif cmd[0] == 'close-db':
        if db.location == 'memory':
            if input('Current database is in memory only; exiting will destroy it. Are you sure? ').lower() not in (
                    'y',
                    'yes'):
                return False
        return True
    elif cmd[0] == 'help':
        prd_help_open()
    return False


def prd_help_open():
    print("""Commands in current context:
        new-image       : Creates a new comparison image. It will only check the HKEYs that the database was created with.
                          Use machine=<id> to specify a specific machine to diff. By default it goes for the machine of 0.
                          "new-image machine=1"

        list-images     : Lists the number of current images in the db and some cursory details.

        diff-images     : Generates a report that compares two different registry images. Enter the image numbers from 
                          list-images as arguments to designate which images to compare. Use "-f filename" to save the report
                          to a file. Examples:
                          "diff-images 0 3" 
                          "diff-images 2 0"
                          "diff-images 1 2 -f registry-report.txt" 

        close-db, exit  : Close this database and prepare to create/load another. Databases in memory will be destroyed.

        new-machine     : Adds a new machine to this database. If given both, the hostname will always be used to connect.
                          Must have either an IP or a hostname:
                          "add-machine ip=192.168.0.10"
                          "add-machine hostname=testmachine01"
                          "add-machine ip=192.168.0.2 hostname=mywinserver01"
                    
                          NOTE: Localhost is by default machine 0. You don't have to add it.

        list-machines   : Prints a list of machines in this database.

        update-machine  : Similar to add machine; except it updates the specified fields. Use the machine ID to specify
                          which machine to edit.
                          "update-machine
        help            : Show this help information


        -f | --file     : Report file name to save to. Will overwrite any existing file.
                          IE:
                         "load-db -f C:\Work\Registry_set.db"
                         "diff-images 1 2 -f registry-report.txt" 
                         
        -q | --quiet    : Suppresses output of errors when using new-image; prevents a diff report from being written to 
                          the screen. 
        
        -i              : Specify a machine ID. Not using this in new-image defaults to localhost (machine 0)
""")


# Main
def main():
    print(header)

    while True:
        cmd = input('> ')
        if process_general_commands(cmd):
            continue
        else:
            break


# program entry point; execution starts here.
if __name__ == '__main__':
    if 'windows' not in system().lower():
        print('This program must be run on a Windows host. Detected \'{} {}\'. Quitting...'.format(system(), release()))
    else:
        main()
