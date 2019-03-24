class DatabaseObject:
    """
    Base class for all objects that directly map to Windows registry objects.
    """
    def __init__(self, **kwargs):
        """
        Creates a new instance from passed in parameters. See implementations for more details on their specific
        argument requirements.
        :param kwargs: The dictionary of arguments.
        """
        self._database_id = int(kwargs.get('dbid'))

    @property
    def dbid(self):
        return self._database_id

    @dbid.setter
    def dbid(self, new_id):
        self._database_id = new_id


class RegistryObject(DatabaseObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
