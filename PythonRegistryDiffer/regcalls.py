import winreg
from PythonRegistryDiffer.key import Key
from PythonRegistryDiffer.keyvalue import KeyValue


def get_key(keypath, computer):
    """
    Creates a Key object based on the key at the specified keyPath.
    :param keypath: The path of the key to get. Must start with an HKEY.
    :param computer: The computer whose registry you want to query.
    :return: A dictionary with the values 'errors' and 'data'. 'data' will be the new Key object (if successful).
    """
    pass


def get_key_value(keypath, valueindex, computer):
    """
    Creates a KeyValue object based on index of the passe
    :param keypath: The path of the key whose value to get. Must start with an HKEY.
    :param valueindex: The index of the value
    :param computer: The computer whose registry you want to query.
    :return: A dictionary with the values 'errors' and 'data'. 'data' will be the new KeyValue object (if successful).
    """
    pass


def get_all_key_values(keypath, computer):
    """
    Creates a list of KeyValue objects with all of the value objects in the specified key.
    :param keypath: The path of the key whose values to get. Must start with an HKEY.
    :param computer: The computer whose registry you want to query.
    :return: A dictionary with the values 'errors' & 'data'. 'data' will be a list of KeyValue objects (if successful).
    """
    pass


def get_all_sub_keys(keypath, computer):
    """
    Creates a list of all subkeys of a key. Each key will be represented by its complete path, including HKEY.
    :param keypath: The key whose sub-keys you want to get. Can be an HKEY.
    :param computer: The computer whose registry you want to query.
    :return: A dictionary with the values 'errors' & 'data'. 'data' will be a list of complete key paths.
    """
    pass
