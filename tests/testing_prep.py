import winreg as r


def reset_all_changes():
    """Removes all of the registry changes that the other module functions make.

    :return: None
    """
    try:
        r.DeleteKey(r.HKEY_CURRENT_USER, 'NewKeyChangeValue\\')
    except FileNotFoundError:
        pass
    try:
        r.DeleteKey(r.HKEY_CURRENT_USER, 'NewKeyDeleteKey\\')
    except FileNotFoundError:
        pass
    try:
        r.DeleteKey(r.HKEY_CURRENT_USER, 'NewKeyDeleteValue\\')
    except FileNotFoundError:
        pass
    try:
        r.DeleteKey(r.HKEY_CURRENT_USER, 'NewKeySame\\')
    except FileNotFoundError:
        pass
    return 'All test keys deleted.'


def before_diff():
    """Adds 4 new keys for testing purposes.

    :return: None
    """
    create_key_with_value('NewKeyChangeValue', 'NewKeyChangeMe', 'Original')
    create_key_with_value('NewKeyDeleteKey', 'NewKeyDeleteMe', 'Key is still here!.')
    create_key_with_value('NewKeyDeleteValue', 'NewKeyDeleteValue', 'Value is still here!')
    create_key_with_value('NewKeySame', 'NewKeyStaysHere', 'Still here! And you shouldn\'t see me!')
    return 'Ready to test first diff.'


def before_second_diff():
    """Deletes one test key and one test value inside of a key. Updates one key value.

    :return: None
    """
    r.DeleteKey(r.HKEY_CURRENT_USER, 'NewKeyDeleteKey\\')
    create_key_with_value('NewKeyDeleteValue\\', 'NewKeyDeleteValue', None)
    create_key_with_value('NewKeyChangeValue\\', 'NewKeyChangeMe', 'Updated')
    return 'Ready to test second diff.'


def create_key_with_value(key_name, key, value):
    """
    Set/Remove Key in windows registry.

    :param key: Run Key Name
    :param value: Program to Run
    :param key_name: Key name within HKCU to create
    :return: None
    """

    r.CreateKey(r.HKEY_CURRENT_USER, key_name)

    reg_key = r.OpenKey(r.HKEY_CURRENT_USER, key_name, 0, r.KEY_SET_VALUE)

    with reg_key:
        if value is None:
            r.DeleteValue(reg_key, key)
        else:
            r.SetValueEx(reg_key, key, 0, r.REG_SZ, value)


def main():
    """Processes user input. Quits when the user exits.

    :return: None
    """
    print('1 = Reset all test changes in the registry.')
    print('2 = Prep the registry for the first diff (or new image).')
    print('3 = Delete or update the test keys.')
    print('4 = Exit.')

    while True:
        _in = input('PyRDT TestPrep> ')
        if _in == '1':
            print(reset_all_changes())
        if _in == '2':
            print(before_diff())
        if _in == '3':
            print(before_second_diff())
        if _in == '4':
            return


if __name__ == '__main__':
    main()
