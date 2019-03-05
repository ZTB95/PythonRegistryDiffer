import PythonRegistryDiffer.RegistryObject as RegistryObject


class KeyValue(RegistryObject):
    def __init__(self, **kwargs):
        """
        Creates a new KeyValue object.
        :param kwargs: Requires name, type, data, and dbid.
        """
        self._name = str
        self._type = int
        self._data = None  # This will vary based on the registry value type.
        self.name = kwargs.get('name')
        self.type = kwargs.get('type')
        self.data = kwargs.get('data')
        super.__init__(**kwargs)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_type):
        self._type = new_type

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data
