from toptica.lasersdk.dlcpro.v2_0_3 import DLCpro, SerialConnection, DeviceNotFoundError


class TopticaDLCPro:
    """Communicate with a Toptica DLC Pro laser controller.

    Author      : Gareth Sion Jones
    Affiliation : University of Oxford
    Date        : July, 2022

    Example:
        >>> toptica = TopticaDLCPro.TopticaDLCPro(com_port='COM1', baud_rate=115200, timeout=5)
        >>> toptica.set_current(55)
        >>> toptica.enable_current(True) # Enable current emission
    """

    def __init__(self, com_port='COM1', baud_rate=115200, timeout=5):
        """Initialize the laser controller

        :param com_port : name of com port
        :param baud_rate : baud rate
        :param timeout : timeout of the instrument
        """
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.dlc = DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout))

    @property
    def comport(self):
        return self.com_port

    @comport.setter
    def comport(self, comport):
        self.com_port = comport

    @property
    def baudrate(self):
        return self.baud_rate

    @baudrate.setter
    def baudrate(self, baudrate):
        self.baud_rate = baudrate

    @property
    def tout(self):
        return self.timeout

    @tout.setter
    def tout(self, tout):
        self.timeout = tout

    def set_current(self, set_current):
        """Set the current of the Toptica laser

        :param set_current (int, float): intended injection current
        """
        try:
            with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
                dlc.laser1.dl.cc.current_set.set(set_current)
        except ConnectionError as e:
            print("Couldn't connect to the Toptica controller")
            print(e)

    def get_current(self):
        """Get the set current of the Toptica laser

        :param get_current (int, float): intended injection current
        :returns set current (float)
        """
        try:
            with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
                return dlc.laser1.dl.cc.current_set.get()
        except ConnectionError as e:
            print("Couldn't connect to the Toptica controller")
            print(e)

        # self.dlc.laser1.dl.cc.current_set(set_current)

    def get_actual_current(self):
        """Get the current measured by the Toptica laser

        :returns : actual current measured by Toptica (float)
        """
        try:
            with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
                return dlc.laser1.dl.cc.current_act.get()
        except ConnectionError as e:
            print("Couldn't connect to the Toptica controller")
            print(e)

    def enable_current(self, enabled=True):
        if not isinstance(enabled, bool):
            raise ValueError('The enabled argument must be of boolean type')
        try:
            with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
                dlc.laser1.dl.cc.enabled.set(enabled)
                print('Current emission enabled' if enabled else 'Current emission disabled')
        except ConnectionError as e:
            print("Couldn't connect to the Toptica controller")
            print(e)

    def set_feedforward(self, ffwd):
        """Set the feedforward factor of the Toptica laser

        :param ffwd (float): intended feedforward factorinjection current
        """
        if not isinstance(ffwd, (int, float)):
            raise ValueError('The ffwd argument must be of int or float type')
        try:
            with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
                dlc.laser1.dl.cc.feedforward_factor.set(ffwd)
        except ConnectionError as e:
            print("Couldn't connect to the Toptica controller")
            print(e)

    def get_feedforward(self):
        """Get the actual feedforward factor of the Toptica controller

        :returns : actual feedforward factor measured by Toptica (float)
        """
        try:
            with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
                return dlc.laser1.dl.cc.feedforward_factor.get()
        except ConnectionError as e:
            print("Couldn't connect to the Toptica controller")
            print(e)

    def enable_feedforward(self, enabled=True):
        if not isinstance(enabled, bool):
            raise ValueError('The enabled argument must be of boolean type')
        try:
            with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
                dlc.laser1.dl.cc.feedforward_enabled.set(enabled)
                print('Feedforward enabled' if enabled else 'Feedforward disabled')
        except ConnectionError as e:
            print("Couldn't connect to the Toptica controller")
            print(e)

    def set_temperature(self, temp_set=20.2):
        """Set the feedforward factor of the Toptica laser

        :param temp_set (float): intended case temperature setting of the Toptica laser
        """
        try:
            with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
                dlc.laser1.dl.tc.temp_set.set(temp_set)
        except ConnectionError as e:
            print("Couldn't connect to the Toptica controller")
            print(e)

    def get_temperature(self):
        """Get the actual case temperature of the Toptica laser

        :returns : actual temperature measured by Toptica (float)
        """
        try:
            with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
                return dlc.laser1.dl.tc.temp_act.get()
        except ConnectionError as e:
            print("Couldn't connect to the Toptica controller")
            print(e)

    def enable_temp_control(self, enabled=True):
        if not isinstance(enabled, bool):
            raise ValueError('The enabled argument must be of boolean type')
        try:
            with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
                dlc.laser1.dl.tc.enabled.set(enabled)
                print('Temp control enabled' if enabled else 'Temp control disabled')
        except ConnectionError as e:
            print("Couldn't connect to the Toptica controller")
            print(e)

    def set_scan(self, amplitude=20, offset=10, freq=0.4, shape=1):
        try:
            with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
                dlc.laser1.scan.amplitude.set(amplitude)
                dlc.laser1.scan.offset.set(offset)
                dlc.laser1.scan.frequency.set(freq)
                dlc.laser1.scan.signal_type.set(shape)  # 0:sine, 1:Triangle, 2:Sawtooth
        except ConnectionError as e:
            print("Couldn't connect to the Toptica controller")
            print(e)

    def enable_scan(self, enabled=True):
        if not isinstance(enabled, bool):
            raise ValueError('The enabled argument must be of boolean type')
        try:
            with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
                dlc.laser1.scan.enabled.set(enabled)
                print('Scan enabled' if enabled else 'Scan disabled')
        except ConnectionError as e:
            print("Couldn't connect to the Toptica controller")
            print(e)

    def get_pc_voltage(self):
        """Get the actual piezo voltage of the Toptica laser

        :returns : actual voltage measured by Toptica (float)
        """
        try:
            with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
                return dlc.laser1.dl.pc.voltage_act.get()
        except ConnectionError as e:
            print("Couldn't connect to the Toptica controller")
            print(e)