import PythonRegistryDiffer.RegistryObject as RegistryObject


class Image(RegistryObject):
    def __init__(self, **kwargs):
        self._taken_time = None
        self._label = str
        self._machine = str

        self.taken_time = kwargs.get('taken_time')
        self.label = kwargs.get('label')
        self.machine = kwargs.get('machine')
        super.__init__(**kwargs)

    @property
    def taken_time(self):
        return self._taken_time

    @taken_time.setter
    def taken_time(self, new_time):
        self._taken_time = new_time

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, new_label):
        self._label = new_label

    @property
    def machine(self):
        return self._machine

    @machine.setter
    def machine(self, new_machine_name):
        self._machine = new_machine_name
