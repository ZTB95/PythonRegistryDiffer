import winreg as wr
import PythonRegistryDiffer.RegistryObject as RegistryObject


class Key(RegistryObject):
    def __init__(self):
        # inherited dbid
        self._key_path = str  # key_path
        self._value_list = []  # values
        self._windows_time = int  # modified
        self._name = str  # name

    def _create_new(self, **kwargs):
        pass

    def _create_from_database(self, **kwargs):
        self.dbid = int(kwargs.get('dbid'))
        self.key_path = str(kwargs.get('key_path'))
        self.values = list(kwargs.get('values'))
        self.modified = int(kwargs.get('modified'))
        self.name = str(kwargs.get('name'))

    @property
    def key_path(self):
        return self._key_path

    @key_path.setter
    def key_path(self, key_path):
        self._key_path = key_path

    @property
    def values(self):
        return self._value_list

    @values.setter
    def values(self, new_list):
        self._value_list = new_list

    @property
    def modified(self):
        return self._windows_time

    @modified.setter
    def modified(self, new_time):
        self._windows_time = new_time

    @property
    def has_values(self):
        if len(self.values) > 0:
            return True
        else:
            return False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name
