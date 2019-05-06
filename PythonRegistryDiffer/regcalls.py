import winreg as wreg
import datetime as dt
from .key import Key
from .keyvalue import KeyValue
from .image import Image
from .machine import Machine


def get_key_value(key_handle, value_index):
    """
    Creates a KeyValue object based on index of the passe
    :param key_handle: The path of the key whose value to get. Must start with an HKEY.
    :param value_index: The index of the value
    :return: A dictionary with the values 'errors' and 'data'. 'data' will be the new KeyValue object (if successful).
    """
    retd = {
        'errors': [],  # dictionary to return
        'data': None
    }

    try:
        values = wreg.EnumValue(key_handle, value_index)  # get the key value from the registry handle
        kv_dict = {
            'name': values[0],  # format the data into a dictionary compatible with KeyValue
            'type': values[2],
            'data': values[1]
        }

        retd['data'] = KeyValue(**kv_dict)  # Create the new KeyValue and update the data key of the return dictionary

    except Exception:  # TODO Going to find out what errors I want to catch during testing; for now just rethrow them.
        retd['errors'].append(Exception)
        raise Exception  # DEBUG TODO remove

    return retd


def get_all_key_values(key_handle):
    """
    Creates a list of KeyValue objects with all of the value objects in the specified key.
    :param key_handle: The path of the key whose values to get. Must start with an HKEY.
    :return: A dictionary with the values 'errors' & 'data'. 'data' will be a list of KeyValue objects (if successful).
    """
    retd = {
        'errors': [],  # dictionary to return
        'data': None
    }

    try:
        num_of_vals = wreg.QueryInfoKey(key_handle)[1]  # Gets the number of key values in a key
        new_key_list = []  # This will be the list that is returned in retd
        error_list = []

        if num_of_vals == 0:  # if there aren't any key values, return the empty dictionary
            return retd

        for index in range(num_of_vals):  # for (the index of) each key values in the key...
            new_key = get_key_value(key_handle, index)  # ...attempt to create a KeyValue instance

            # if the returned no errors and data is an instance of KeyValue, add it to the new_key_list
            if new_key['errors'] is None and isinstance(new_key['data'], KeyValue):
                new_key_list.append(new_key['data'])
            else:
                error_list.extend(new_key['errors'])

    # there should only ever be exceptions here if get_key_value fails to catch one, or if QueryInfoKey fails.
    except Exception:  # TODO finish
        retd['errors'].append(Exception)
        raise Exception  # DEBUG TODO remove

    return retd


def get_key(parent_key_handle, key_name, key_path):
    """
    Creates a Key object based on the key based on the parent key and key name.
    Does not validate key_path's accuracy.
    :param parent_key_handle: a winreg handle for the parent key (or HKEY handle if a first-level key)
    :param key_path: The path of the key to get. Must start with an HKEY.
    :param key_name: The name of the key to get
    :return: A dictionary with the values 'errors' and 'data'. 'data' will be the new Key object (if successful).
    """
    retd = {
        'errors': [],  # dictionary to return
        'data': None
    }

    try:
        new_key_handle = wreg.OpenKey(parent_key_handle, key_name)  # ...attempt to create a KeyValue instance
        new_key_time = wreg.QueryInfoKey(new_key_handle)[2]  # Gets the modified time of the key

        key_val_dict = get_all_key_values(new_key_handle)  # run get_all_key_values and save the dict
        key_values = key_val_dict['data']  # get the data out (List of KeyValues or empty list)
        if len(key_val_dict['errors']) > 0:  # if errors occurred while getting key values, pass them up.
            retd['errors'].extend(key_val_dict['errors'])

        # Crate the new Key dictionary
        new_key_dict = {
            'key_path': key_path,
            'values': key_values,
            'modified': new_key_time,
            'name': key_name
        }

        new_key = Key(**new_key_dict)  # Create a new instance of Key with the new_key_dict

        retd['data'] = new_key  # add the new Key instance to the return dictionary

    except Exception:  # TODO finish
        retd['errors'].append(Exception)
        raise Exception  # DEBUG TODO remove

    return retd


def get_all_sub_keys(r_key_handle, r_key_name):
    """
    Creates a list of all subkeys of a key (and their values). Uses instances of Key and KeyValue
    :param r_key_handle: An established winreg registry key handle.
    :param r_key_name: The string name of the key.
    :return: A dictionary with the values 'errors' & 'data'. 'data' will be a list of complete key objects.
    """
    retd = {
        'errors': [],  # dictionary to return
        'data': None
    }

    # I took this from my prototype edition of this program that was all inside of 2 files and completely hacked
    # together. It used to just get the string names, but not It's hacked slightly more to get it to fit in here.
    # Forgive me...
    # TODO make this not a pile of steaming hot garbage with sewage on top. Maybe just clean up the sewage spill...

    recursion_level = 1  # keep recursion issues at bay... maybe

    def get_sub_key_list(key_handle, key_name):
        """
        Creates a list of all subkeys of a key (and their values). Uses instances of Key and KeyValue
        :param key_handle: An established winreg registry key handle.
        :param key_name: The string name of the key.
        :return: None (appends to retd)`
        """
        global recursion_level

        if recursion_level > 512:
            raise RecursionError(
                'Recursion error while trying to get a list of subkeys. Depth > 512.\nLast key: {}'.format(
                    key_name)
            )

        cur_key_info = wreg.QueryInfoKey(key_handle)
        _key_list = []
        subkey_num = cur_key_info[0]  # number of subkeys

        if subkey_num == 0:
            recursion_level -= 1
            return

        for i in range(subkey_num):  # for each sub-key
            reg2 = wreg.EnumKey(key_handle, i)  # get the subkey's name

            key_location = '{}{}\\'.format(key_name, reg2)  # reconstruct its location

            new_key = get_key(key_handle, reg2, key_location)  # create a RegKey class instance (including KeyValues)

            if len(new_key['errors']) == 0:
                _key_list.append(new_key['data'])  # save the new key.
            else:
                retd['errors'].extend(new_key['errors'])

            try:
                recursion_level += 1
                get_sub_key_list(wreg.OpenKey(key_handle, reg2), key_location)
            except WindowsError:
                retd['errors'].append(WindowsError('Permissions error trying to access key: {}'.format(key_location)))
                recursion_level -= 1

    get_sub_key_list(r_key_handle, r_key_name)

    return retd


def get_registry_image(machine, hklm, hku, hkcu, hkcc, hkcr, label=''):
    """
    Returns a registry image object
    It will continue past any non-fatal registry errors.
    :param machine: The target machine.
    :param hklm: Boolean - to get the HKLM Key or not.
    :param hku: Boolean - to get the HKU Key or not.
    :param hkcu: Boolean - to get the HKCU Key or not.
    :param hkcc: Boolean - to get the HKCC Key or not.
    :param hkcr: Boolean - to get the HKCR Key or not.
    :param label: String - optional. Default is an empty string.
    :return: A dictionary with the values 'errors' & 'data'. 'data' will be an Image instance.
    """
    retd = {  # dictionary to return
        'errors': [],
        'data': None
    }
    target_ip = ''  # the target IP. This is the machine who's registry will be enumerated.
    image_params = {  # the parameters that will be passed into the Image instance.
        'taken_time': dt.datetime.now(),
        'machine': machine.dbid,
        'label': label,
        'keys': []
    }

    # Open the registry handle
    if machine.hostname == 'localhost':
        target_ip = None  # this is what winreg is expecting for localhost
    else:
        target_ip = '\\\\{}'.format(str(machine.last_ip))  # Winreg expects the format '\\<hostname>|<ip>' or None

    # DRY enumeration for each HKEY TODO: Handle failed connection errors.
    def enum_registry(hkey_root):
        registry = wreg.ConnectRegistry(target_ip, hkey_root)  # Open the registry handle
        enum_dict = get_all_sub_keys(registry, hkey_root)  # enumerate all of its subkeys
        image_params['keys'].extend(enum_dict['data'])  # save the data
        retd['errors'].extend(enum_dict['errors'])  # save the errors

    # If an HKEY is set to True, enumerate it.
    if hklm:
        enum_registry(wreg. HKEY_LOCAL_MACHINE)
    if hku:
        enum_registry(wreg.HKEY_USERS)
    if hkcu:
        enum_registry(wreg.HKEY_CURRENT_USER)
    if hkcc:
        enum_registry(wreg.HKEY_CURRENT_CONFIG)
    if hkcr:
        enum_registry(wreg.HKEY_CLASSES_ROOT)

    retd['data'] = Image(**image_params)
    return retd
