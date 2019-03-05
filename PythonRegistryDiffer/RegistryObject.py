class RegistryObject:
    """
    Base class for all objects that directly map to Windows registry objects.
    """
    def __init__(self):
        """
        Creates a new instance from either 1) passed in parameters or 2) a single argument that represents which object
        in the registry to create. See implementations for more details on their specific argument needs.
        :param kwargs: The dictionary of arguments.
        """
        self._database_id = 0

    @property
    def dbid(self):
        return self._database_id

    @dbid.setter
    def dbid(self, new_id):
        self._database_id = new_id