import winreg as wr
import PythonRegistryDiffer.RegistryObject as RegistryObject


class Key(RegistryObject):
    def __init__(self):
        self._key_path = str
        self._value_list = []
        self._windows_time = int

    def _create_new(self, **kwargs):
        pass

    def _create_from_database(self, **kwargs):
        pass

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
