class RegistryObject:
    """
    Base class for all objects that directly map to Windows registry objects.
    """
    def __init__(self, **kwargs):
        """
        Creates a new instance from either 1) passed in parameters or 2) a single argument that represents which object
        in the registry to create. See implementations for more details on their specific argument needs.
        :param kwargs: The dictionary of arguments.
        """
        self.database_id = 0

        if len(kwargs) > 1:
            self._create_from_database(**kwargs)
        elif len(kwargs) == 1:
            self._create_new(**kwargs)
        elif len(kwargs) <= 0:
            raise KeyError

    def _create_new(self, **kwargs):
        raise NotImplementedError

    def _create_from_database(self, **kwargs):
        raise NotImplementedError

