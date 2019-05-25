# This module is here because I don't like cluttered run modules.
# Also all, some of these functions could be used by any other script or program that implements this package.
from .machine import Machine
from .key import Key
from .keyvalue import KeyValue
from .regcalls import get_registry_image as gri


def new_image(machine_id, db):
    """
    Creates and inserts a live registry image into the database.
    :param machine_id: The ID of the machine that will have an image taken.
    :param db: An open database object.
    :return: The new Image's database ID.
    """  # TODO update regcalls gri to check for ip or hostname. Use hostname by default.
    mach = db.get_machine(machine_id)  # get the database object that regcalls.py needs.
    retd = gri(mach, hklm=db.hklm, hkcu=db.hkcu, hku=db.hku, hkcc=db.hkcc, hkcr=db.hkcr)
    if retd['errors'].count() is not 0:
        for error in retd['errors']:  # TODO remove this if you're using this package in a different program
            print(error)

    if retd['data'] is not None:
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


def list_of_images(db, machine_id=None):
    """
    Gets a formatted list of images (as a string).
    :param db: An open database object.
    :param machine_id: Set this to a machine's ID to restrict the pull to a specific machine
    :return: string
    """
    images = db.get_image_list()  # gets the list of images (does NOT get their keys)
    ret_string = 'Machine ID - Image ID - Time Taken - Label'

    # TODO Adjust the formatting of the display.
    if machine_id is not None:
        images_copy = images  # can't iterate over a list that is being modified.
        for image in images_copy:
            if image.machine != machine_id:
                images.remove(image)  # test this. It might not be pointing to the same image objects in memory. It should, though.

    for image in images:
        ret_string += "{}\t{}\t{}\t{}\n".format(image.dbid, image.machine, image.label, image.taken_time)

    return ret_string


def list_of_machines(db):
    """
    Gets a formatted list of machines (as a string).
    :param db: An open database object.
    :return: string
    """
    machines = db.get_machine_list()  # gets the list of machines (does NOT get their images)
    ret_string = 'Machine ID - Last Known IP - Hostname - Image Count'

    for machine in machines:
        image_count = db.get_count_of_machines_images_by_machine_id(machine.dbid)
        ret_string += "{}\t{}\t{}\t{}\n".format(machine.dbid, machine.last_ip, machine.hostname, image_count)

    return ret_string


def diff_images(db, image_1_id, image_2_id, report_type='CSV'):
    """
    Diffs two images and returns a report.
    :param db: An open database object
    :param image_1_id: DBID of the first image to diff
    :param image_2_id: DBID of the second image to diff
    :param report_type: Currently only supports CSV.
    :return: A string object that contains the fully-built report.
    """
    def _create_key_and_value_string(key):
        """
        Returns a string that represents a key and its values. Used by various diff functions.
        :param key: The key to write a string for
        :return: String
        """
        def _create_value_string(key_string, value):
            return ",{},{},{},{}\n".format(key_string, value.name, value.type, str(value.data))

        key_string = "{},{},{},{},{}".format(key.dbid, key.name, key.has_values, key.modified, key.key_path)

        retobj = ''

        # for each value in the key (if any), create a value string and append it to the return object
        if key.has_values is True:
            for value in key.values:
                retobj += _create_value_string(key_string, value)
        else:  # key_string doesn't have a newline at the end of it because if there are values in the key, they add it
            retobj = key_string + '\n'  # so if there's no keys, we have to add a newline ourselves.

        return retobj

    # TODO: Complete these functions
    def _write_key_to_csv_diff_report(first_key=None, second_key=None):
        """
        Adds two diff'ed keys found to bew new or deleted to the CSV report
        :param first_key: The first key (or none if it wasn't found)
        :param second_key: The second key (or none if it wasn't found)
        :return: None
        """

    def _write_images_to_csv_diff_report(image_1, image_2):
        """
        Writes image headers to the report (CSV type).
        :param image_1: The first image
        :param image_2: The second image
        :return: None
        """
        def _create_image_string(image):
            return "{},{},{},{}\n".format(image.dbid, image.machine, image.label, image.taken_time)

        retobj = 'Image DBID,Machine ID,Label,Time Taken'
        retobj += _create_image_string(image_1)
        retobj += _create_image_string(image_2)

        return retobj

    def _find_keys_that_were_deleted_or_added(key_list_1, key_list_2):
        """
        Finds keys that were deleted or added, then adds them to the proper report type
        :param key_list_1: The key list for the first image
        :param key_list_2: The key list for the second image
        :return: None
        """
        pass

    def _find_keys_whose_values_have_changed(key_list_1, key_list_2):
        """
        Finds keys whose values have changed
        :param key_list_1: The key list for the first image
        :param key_list_2: The key list for the second image
        :return: None
        """
        pass

    def _find_keys_whose_metadata_has_changed_but_not_the_values(key_list_1, key_list_2):
        """
        Finds keys that have metadata changes but all values are the same.
        :param key_list_1: The key list for the first image
        :param key_list_2: The key list for the second image
        :return: None
        """
        pass

    ## Execution starts here ##
    diff_report = ''  # The report is held in this
    dbids_of_keys_already_identified = []  # list of DBID's of keys already identified as changed/deleted/added

    # get the images so we can put there data at the top of the report.
    image_1 = db.get_image(image_1_id)
    image_2 = db.get_image(image_2_id)

    if report_type == 'CSV':
        diff_report += _write_images_to_csv_diff_report(image_1, image_2)
    else:
        raise ValueError("Unsupported report type given: {}".format(report_type))

    image_1_keys = db.get_key_list(image_1_id)
    image_2_keys = db.get_key_list(image_2_id)

    _find_keys_that_were_deleted_or_added(image_1_keys, image_2_keys)
    _find_keys_whose_values_have_changed(image_1_keys, image_2_keys)
    _find_keys_whose_metadata_has_changed_but_not_the_values(image_1_keys, image_2_keys)

    return diff_report

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
