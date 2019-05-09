from .machine import Machine
from .regcalls import get_registry_image as gri


def new_image(machine_id, db):
    """
    Creates and inserts a live registry image into the database.
    :param machine_id: The ID of the machine that will have an image taken.
    :param db: An open database object.
    :return: The new Image's database ID.
    """  # TODO update regcalls gri to check for ip or hostname. Use hostname by default.
    mach = db.get_machine(machine_id)  # get the database object that regcalls.py needs.
    gri(mach, hklm=db.hklm, hkcu=db.hkcu, hku=db.hku, hkcc=db.hkcc, hkcr=db.hkcr)
    return db.add_image(gri)


def new_machine(ip, hostname, db):
    """
    Creates a new machine in the database and returns and object.

    :param ip: The IP address of the machine (can be None if hostname is not)
    :param hostname: The hostname of the machine (can be None if IP is not).
    :param db: An open database object.
    :return: The new machine's database ID.
    """
    mach = Machine(ip=ip, hostname=hostname)  # creates the machine object
    return db.add_machine(mach)  # inserts it into the database and return's the new machine's database ID


def list_of_images(db, machine_id=0):
    """
    Gets a formatted list of images (as a string).
    :param db: An open database object.
    :param machine_id: Set this to a machine's ID to restrict the pull to a specific machine
    :return: string
    """
    images = db.get_image_list()  # gets the list of images (does NOT get their keys)
    ret_string = 'Machine ID - Image ID - Time Taken - Label'

    # TODO Adjust the formatting of the display.
    for image in images:
        ret_string += "{}\t{}\t{}\t{}\n".format(image.machine, image.dbid, image.taken_time, image.label)

    return ret_string


def diff_images():
    pass


def prd_help():
    print("""USAGE:

        new-database : Creates a new database to host images of the registry. Requires the use of -f or -m.

        new-image   : Creates a new comparison image. It will only check the HKEYs that the first image was 
                     created with. Note: You don't need to call this option to create the first image; new-db creates
                     a baseline image unless called with the -e option.

        list-images : Lists the number of current images in the db and some cursory details.

        diff-images : Generates a report that compares two different registry images. Enter the image numbers from 
                     list-images as arguments to designate which images to compare. Use "-f filename" to save the report
                     to a file. Examples:
                    "PythonRegistryDiffer> diff-images 0 3" 
                    "PythonRegistryDiffer> diff-images 2 0"
                    "PythonRegistryDiffer> diff-images 1 2 -f registry-report.txt" 

        load-db    : Loads an existing baseline (and any previously saved comparison images) from the specified file.
                      *-f filename
                      *Not using -f will reload the current db's save file without saving any changes made in the
                       current session.

        save-db    : Save changes to this db.
                      *-f filename
                      *Not using -f will save to the existing save file

        -h | help        : Show this help information

OPTIONS:

        -f | --file <filename> : The database or report file to use/save as/load from
                      IE:
                      "PythonRegistryDiffer> load-db -f C:\Work\Registry_set.db"
                      "PythonRegistryDiffer> save-db -f file_in_current_dir.db"
                      "PythonRegistryDiffer> diff-images 1 2 -f registry-report.txt" 

        <only for use with the 'new-db' or 'list-images' command>
        --no-hklm : Exclude the HKEY_LOCAL_MACHINE root key.
           *hkcc : Exclude the HKEY_CURRENT_CONFIG root key.
           *hkcr : Exclude the HKEY_CLASSES_ROOT root key.
           *hku  : Exclude the HKEY_USER root key.
           *hkcu : Exclude the HKEY_CURRENT_USER root key.
        
        -v | --verbose 	: Print all errors to the screen as they occur.
        
        -q | --quiet 		: Suppress printing any information about non-fatal errors.
        
        -m | --memorymode   : Keeps the database in memory mode instead of saving it.
        
        -e | --empty		: Skips creating a baseline image when calling new-database.
        
        -r | --remote       : Attempts to connect to a remote machine and get images from its registry.""")
