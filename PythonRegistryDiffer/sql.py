# CREATES
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
                     ');\n')  # TODO: Remove the name column from the DBD and update the table's name

_create_key_value_table = ('CREATE TABLE RegKeyValue ( '  # TODO: Update the table's name in the DBD
                           'id INTEGER PRIMARY KEY, '
                           'FOREIGN KEY (regKeyId) REFERENCES RegKey(id) ENFORCED, ' # TODO: update the column name in the DBD
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

create_database = _create_machine_table + \
                  _create_image_table + \
                  _create_key_table + \
                  _create_key_value_table + \
                  _create_hkeys_table + \
                  _create_only_one_hkey_trigger

# SELECTS
select_all_from_machine_by_id = ('SELECT * '
                                 'FROM Machine '
                                 'WHERE id =?')

select_all_from_regimage_by_id = ('SELECT * '
                                  'FROM RegImage '
                                  'WHERE id=? ')

select_all_from_regkey_by_id = ('SELECT * '
                                'FROM RegKey '
                                'WHERE id=?')

select_all_from_regkeyvalue_by_id = ('SELECT * '
                                     'FROM RegKeyValue '
                                     'WHERE id=? ')

select_all_from_hkeys_by_id = ('SELECT * '
                               'FROM HKEYs '
                               'WHERE i =? ')

select_all_children_of_machine_by_id = ('SELECT * '
                                        'FROM RegImage '
                                        'WHERE machineId=? ')

select_all_children_of_machine = ('SELECT * '
                                  'FROM RegImage ')

select_all_children_of_regimage_by_id = ('SELECT * '
                                         'FROM RegKey '
                                         'WHERE imageId=? ')

select_all_children_of_regkey_by_id = ('SELECT * '
                                       'FROM RegKeyValue '
                                       'WHERE regKeyId=? ')

select_newest_in_machine = ('SELECT * '
                            'FROM Machine'
                            'WHERE id=(SELECT MAX(id) from Machine) ')

select_newest_in_regimage = ('SELECT * '
                             'FROM RegImage'
                             'WHERE id=(SELECT MAX(id) from RegImage) ')

select_newest_in_regkey = ('SELECT * '
                           'FROM RegKey'
                           'WHERE id=(SELECT MAX(id) from RegKey) ')

select_newest_in_regkeyvalue = ('SELECT * '
                                'FROM RegKeyValue'
                                'WHERE id=(SELECT MAX(id) from RegKeyValue) ')

select_hkeys = ('SELECT * '
                'FROM hkeys'
                'WHERE id=(SELECT MAX(id) from hkeys) ')

# INSERTS
insert_into_machine = 'INSERT INTO Machine VALUES (?, ?)'

insert_into_regimage = 'INSERT INTO RegImage VALUES (?, ?, ?)'

insert_into_regkey = 'INSERT INTO RegKey VALUES (?, ?, ?, ?)'

insert_into_regkeyvalue = 'INSERT INTO RegKeyValue VALUES (?, ?, ?, ?)'

insert_hkeys = 'INSERT INTO HKEYs VALUES (?, ?, ?, ?, ?)'
