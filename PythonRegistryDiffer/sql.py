# CREATES
create_machine_table = ('CREATE TABLE Machine ( '
                        'id INTEGER PRIMARY KEY, '
                        'lastKnownIP VARCHAR(46), '
                        'hostName VARCHAR(256) '
                        ');\n')

create_image_table = ('CREATE TABLE RegImage ( '  # TODO Update the tables name in the DBD
                      'id INTEGER PRIMARY KEY, '
                      'machineId INTEGER, '
                      'label VARCHAR(256) NULL, '
                      'timeTaken DATETIME NOT NULL, '
                      'FOREIGN KEY(machineId) REFERENCES Machine(id) '
                      ');\n')

create_key_table = ('CREATE TABLE RegKey ( '
                    'id INTEGER PRIMARY KEY, '
                    'regImageId INTEGER, '
                    'path VARCHAR(256) NOT NULL , '
                    'lastModified DATETIME NOT NULL,'
                    'name VARCHAR(256) NOT NULL, '
                    'FOREIGN KEY(regImageId) REFERENCES RegImage(id) '
                    ');\n')  # TODO: update the table's name
                    # TODO: alter the entire app to get RegKey's name from its path - it's already there.

create_key_value_table = ('CREATE TABLE RegKeyValue ( '  # TODO: Update the table's name in the DBD
                          'id INTEGER PRIMARY KEY, '
                          'regKeyId INTEGER, ' # TODO: update the column name in the DBD
                          'name VARCHAR(256) NOT NULL, '
                          'type INTEGER NOT NULL, '
                          'data BLOB(1048576) NOT NULL, '  # 1 MB should be enough for anything in a REG_BINARY key, right? TODO: try to break this
                          'FOREIGN KEY (regKeyId) REFERENCES RegKey(id) '
                          ');\n')

create_hkeys_table = ('CREATE TABLE HKEYs ( '
                      'id INTEGER PRIMARY KEY, '
                      'hklm BOOLEAN NOT NULL, '
                      'hkcu BOOLEAN NOT NULL, '
                      'hku BOOLEAN NOT NULL, '
                      'hkcr BOOLEAN NOT NULL, '
                      'hkcc BOOLEAN NOT NULL '
                      ');\n')

create_only_one_hkey_trigger = ("CREATE TRIGGER trg_onlyOneHKEY "
                                "BEFORE INSERT "
                                "ON HKEYs "
                                "WHEN (SELECT COUNT(*) FROM HKEYs) >= 1 "
                                "BEGIN "
                                "SELECT RAISE(FAIL, 'There can only be one row in HKEYs.') "
                                "END; "
                                "END;")

enforce_foreign_keys = 'PRAGMA foreign_keys = 1'

# SELECTS
select_all_from_machine_by_id = ('SELECT * '
                                 'FROM Machine '
                                 'WHERE id = ?')

select_all_from_regimage_by_id = ('SELECT * '
                                  'FROM RegImage '
                                  'WHERE id = ? ')

select_all_from_regkey_by_id = ('SELECT * '
                                'FROM RegKey '
                                'WHERE id = ? ')

select_all_from_regkeyvalue_by_id = ('SELECT * '
                                     'FROM RegKeyValue '
                                     'WHERE id = ? ')

select_all_from_hkeys_by_id = ('SELECT * '
                               'FROM HKEYs '
                               'WHERE id = ? ')

select_all_children_of_machine_by_id = ('SELECT * '
                                        'FROM RegImage '
                                        'WHERE machineId= ? ')

select_all_children_of_machine = ('SELECT * '
                                  'FROM RegImage ')

select_all_children_of_regimage_by_id = ('SELECT * '
                                         'FROM RegKey '
                                         'WHERE imageId=? ')

select_all_children_of_regkey_by_id = ('SELECT * '
                                       'FROM RegKeyValue '
                                       'WHERE regKeyId = ? ')

select_newest_in_machine = ('SELECT MAX(id) '
                            'FROM Machine ')

select_newest_in_regimage = ('SELECT MAX(id) '
                             'FROM RegImage')

select_newest_in_regkey = ('SELECT MAX(id) '
                           'FROM RegKey')

select_newest_in_regkeyvalue = ('SELECT MAX(id) '
                                'FROM RegKeyValue')

select_hkeys = ('SELECT * '
                'FROM hkeys ')

select_number_of_images_a_machine_has = ('SELECT COUNT(*) '
                                         'FROM RegImage '
                                         'WHERE machineId = ? ')

# INSERTS
insert_into_machine = 'INSERT INTO Machine(lastKnownIP, hostname) VALUES (?, ?)'

insert_into_regimage = 'INSERT INTO RegImage(machineId, label, timeTaken) VALUES (?, ?, ?)'

insert_into_regkey = 'INSERT INTO RegKey(regImageId, path, lastModified, name) VALUES (?, ?, ?, ?)'

insert_into_regkeyvalue = 'INSERT INTO RegKeyValue(regKeyId, name, type, data) VALUES (?, ?, ?, ?)'

insert_hkeys = 'INSERT INTO HKEYs(hklm, hkcu, hku, hkcr, hkcc) VALUES (?, ?, ?, ?, ?)'
