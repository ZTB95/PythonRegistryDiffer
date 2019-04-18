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
    retd = {'errors': None,  # dictionary to return
            'data': None}

    try:
        values = wreg.EnumValue(key_handle, value_index)  # get the key value from the registry handle
        kv_dict = {'name': values[0],  # format the data into a dictionary compatible with KeyValue
                   'type': values[2],
                   'data': values[1]}

        retd['data'] = KeyValue(kv_dict)  # Create the new KeyValue and update the data key of the return dictionary

    except Exception:  # TODO Going to find out what errors I want to catch during testing; for now just rethrow them.
        retd['errors'] = Exception
        raise Exception  # DEBUG TODO remove

    return retd


def get_all_key_values(key_handle):
    """
    Creates a list of KeyValue objects with all of the value objects in the specified key.
    :param key_handle: The path of the key whose values to get. Must start with an HKEY.
    :return: A dictionary with the values 'errors' & 'data'. 'data' will be a list of KeyValue objects (if successful).
    """
    retd = {'errors': None,  # dictionary to return
            'data': None}

    try:
        num_of_vals = wreg.QueryInfoKey(key_handle)[1]  # Gets the number of key values in a key
        new_key_list = []  # This will be the list that is returned in retd
        error_list = []

        for index in num_of_vals:  # for (the index of) each key values in the key...
            new_key = get_key_value(key_handle, index)  # ...attempt to create a KeyValue instance

            # if the returned no errors and data is an instance of KeyValue, add it to the new_key_list
            if new_key['errors'] is None and isinstance(new_key['data'], KeyValue):
                new_key_list.append(new_key['data'])
            else:
                error_list.append(new_key['errors'])

    # there should only ever be exceptions here if get_key_value fails to catch one, or if QueryInfoKey fails.
    except Exception:  # TODO finish
        retd['errors'].append(Exception)
        raise Exception  # DEBUG TODO remove

    return retd


def get_key(keypath):
    """
    Creates a Key object based on the key at the specified keyPath.
    :param keypath: The path of the key to get. Must start with an HKEY.
    :param computer: The computer whose registry you want to query.
    :return: A dictionary with the values 'errors' and 'data'. 'data' will be the new Key object (if successful).
    """
    pass


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
