from .base_classes import DatabaseObject


class Machine(DatabaseObject):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._last_ip = str
        self._hostname = str
        self.last_ip = kwargs.get('ip')
        self.hostname = kwargs.get('hostname')

    @property
    def last_ip(self):
        return self._last_ip

    @last_ip.setter
    def last_ip(self, new):
        self._last_ip = new

    @property
    def hostname(self):
        return self._hostname

    @hostname.setter
    def hostname(self, new):
        self.hostname = new
