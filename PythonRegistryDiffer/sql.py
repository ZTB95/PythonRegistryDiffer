

_create_machine_table = ('CREATE TABLE Machine ( '
                         'id INTEGER PRIMARY KEY, '
                         'lastKnownIP VARCHAR(46), '
                         'hostName VARCHAR(256) '
                         ');\n')

_create_image_table = ('CREATE TABLE RegImage ( '  # TODO Update the tables name in the DBD
                       'id INTEGER PRIMARY KEY, '
                       'FOREIGN KEY(machineId) REFERENCES Machine(id) ENFORCED,'
                       'label VARCHAR(256) NULL, '
                       'timeTaken DATETIME NOT NULL '
                       ');\n')

_create_key_table = ('CREATE TABLE RegKey ( '
                     'id INTEGER PRIMARY KEY, '
                     'FOREIGN KEY (regImageId) REFERENCES RegImage(id) ENFORCED, '
                     'path VARCHAR(256) NOT NULL , '
                     'lastModified DATETIME NOT NULL '
                     ');\n')  # TODO Remove the name column from the DBD and update the table's name

_create_key_value_table = ('CREATE TABLE RegKeyValue ( '  # TODO Update the table's name in the DBD
                           'id INTEGER PRIMARY KEY, '
                           'FOREIGN KEY (regKeyId) REFERENCES RegKey(id) ENFORCED, '
                           'name VARCHAR(256) NOT NULL, '
                           'type INTEGER NOT NULL, '
                           'data BLOB(1048576) NOT NULL '  # 1 MB should be enough for anything in a REG_BINARY key, right? TODO: try to break this
                           ');\n')

_create_hkeys_table = ('CREATE TABLE HKEYs ( '
                       'id INTEGER PRIMARY KEY, '
                       'hklm BOOLEAN NOT NULL, '
                       'hkcu BOOLEAN NOT NULL, '
                       'hku BOOLEAN NOT NULL, '
                       'hkcr BOOLEAN NOT NULL, '
                       'hkcc BOOLEAN NOT NULL '
                       ');\n')

_create_only_one_hkey_trigger = ("CREATE TRIGGER trg_onlyOneHKEY BEFORE INSERT "
                                 "ON HKEYs "
                                 "WHEN (SELECT COUNT(*) FROM HKEYs) >= 1 "
                                 "BEGIN "
                                 "SELECT RAISE(FAIL, 'There can only be one row in HKEYs.') "
                                 "END;\n")

_get_key_by_id = ('SELECT * '
                  'FROM RegKey '
                  'WHERE ID = % '
                  ';')

def get_new_database_sql():
    ret = _create_machine_table + \
          _create_image_table + \
          _create_key_table + \
          _create_key_value_table + \
          _create_hkeys_table + \
          _create_only_one_hkey_trigger
    return ret


def get_select_key_by_id(id):
    return _get_key_by_id.replace('%', str(int(id)))