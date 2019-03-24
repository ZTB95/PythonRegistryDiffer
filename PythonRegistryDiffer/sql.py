from .image import Image
from .key import Key
from .keyvalue import KeyValue
from .database import Machine

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

_select_all_from_table_by_id = ('SELECT * '
                                'FROM %table% '
                                'WHERE %id_of% = %id_get% '
                                ';')

_select_newest_id_in_table = ('')

_insert_into_machine = ('')

_insert_into_image = ('')

_insert_into_key = ('')

_insert_into_value = ('')

_insert_into_hkeys = ('')


def create_database_sql(hklm, hkcu, hku, hkcr, hkcc):
    """
    Returns a string of SQL that will create a new database.
    :return: sql string
    :param hklm: bool / is this hkey is going to be queried for this database.
    :param hkcu: bool / is this hkey is going to be queried for this database.
    :param hku: bool / is this hkey is going to be queried for this database.
    :param hkcr: bool / is this hkey is going to be queried for this database.
    :param hkcc: bool / is this hkey is going to be queried for this database.
    """
    ret = _create_machine_table + \
          _create_image_table + \
          _create_key_table + \
          _create_key_value_table + \
          _create_hkeys_table + \
          _create_only_one_hkey_trigger
    return ret


def select_all_from_table_by_id_sql(table, id):
    """
    :param table: The table to select from.
    :param id: The DBID of the object to get.
    :return: A string of SQL.
    """
    sql = _select_all_from_table_by_id.replace('%table%', str(table))
    sql = sql.replace('%id_get%', str(int(id)))
    return sql


def select_all_from_table_by_parent_id(table, parent_id):
    """
    :param table: The table to select from. (The child table.)
    :param parent_id: The ID of the parent item in the parent table to get children of.
    :return: A string of SQL.
    """
    sql = _select_all_from_table_by_id.replace('%table%', str(table))
    if table.lower == 'regkeyvalue':
        sql = sql.replace('%id_of', 'RegKeyId')
    elif table.lower == 'regkey':
        sql = sql.replace('%id_of%', 'RegImageId')
    elif table.lower == 'regimage':
        sql = sql.replace('%id_of', 'machineId')
    else:
        from sqlite3 import DatabaseError
        raise DatabaseError

    sql = sql.replace('%id_get$', str(int(id)))


def select_id_of_newest_item_in_table(table):
    """
    :param table: The table to get the newest item ID of.
    :return: A string of SQL.
    """
    return _select_newest_id_in_table.replace('%table%', table)


def insert_new_object_into_table(object):
    """
    :param object: The object to insert into the table.
    :return: A string of SQL
    """
    if isinstance(object, KeyValue):
        pass
    elif isinstance(object, Key):
        pass
    elif isinstance(object, Image):
        pass
    elif isinstance(object, Machine):
        pass
