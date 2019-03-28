class MappedToDatabase:
    """
    Base class for all objects that directly map to Windows registry objects.
    """
    def __init__(self, **kwargs):
        """
        Creates a new instance from passed in parameters. See implementations for more details on their specific
        argument requirements.
        :param kwargs: The dictionary of arguments.
        """
        try:
            self._database_id = int(kwargs.get('dbid'))
        except Exception:
            self._database_id = None

    @property
    def dbid(self):
        return self._database_id

    @dbid.setter
    def dbid(self, new_id):
        self._database_id = new_id


class RegistryObject(MappedToDatabase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# TODO: Update the documentation here.