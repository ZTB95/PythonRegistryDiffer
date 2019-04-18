import winreg as wreg
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

        retd['data'] = KeyValue(kv_dict)  # Create the new KeyValue and update the data key of the return dictionary

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
        if len(key_values['errors']) > 0:  # if errors occurred while getting key values, pass them up.
            retd['errors'].extend(key_values['errors'])

        # Crate the new Key dictionary
        new_key_dict = {
            'key_path': key_path,
            'values': key_values,
            'modified': new_key_time,
            'name': key_name
        }

        new_key = Key(new_key_dict)  # Create a new instance of Key with the new_key_dict

        retd['data'] = new_key  # add the new Key instance to the return dictionary

    except Exception:  # TODO finish
        retd['errors'] = Exception
        raise Exception  # DEBUG TODO remove

    return retd


def get_all_sub_keys(keypath):
    """
    Creates a list of all subkeys of a key. Each key will be represented by its complete path, including HKEY.
    :param keypath: The key whose sub-keys you want to get. Can be an HKEY.
    :param computer: The computer whose registry you want to query.
    :return: A dictionary with the values 'errors' & 'data'. 'data' will be a list of complete key paths.
    """
    pass


def get_registry(machine):
    """
    Returns a registry image object
    It will continue past any non-fatal registry errors.
    :param database: The database to add a registry image to.
    :param machine: The target machine.
    :return: A list of errors (if any)
    """
