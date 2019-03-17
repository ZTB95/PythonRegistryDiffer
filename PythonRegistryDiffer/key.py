import PythonRegistryDiffer.registryobject as RegistryObject


class Key(RegistryObject.RegistryObject):
    def __init__(self, **kwargs):
        """
        Creates a new Key object.
        :param kwargs: required: dbid, key_path, values, modified, name. A dbid of 0 indicates that the key is not in a
        database.
        """
        self._key_path = str  # key_path
        self._value_list = []  # values
        self._windows_time = int  # modified
        self._name = str  # name
        # self.has_values is derived from self.values' length
        self.key_path = str(kwargs.get('key_path'))
        if kwargs.get('values') is not None:
            self.values = list(kwargs.get('values'))
        self.modified = int(kwargs.get('modified'))
        self.name = str(kwargs.get('name'))
        super().__init__(**kwargs)

    def __eq__(self, other):
        return self.name == other.name and \
               self.key_path == other.key_path and \
               self.modified == other.modified and \
               self.values == other.values

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
