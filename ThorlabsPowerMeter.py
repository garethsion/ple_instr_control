import pyvisa as visa
from ThorlabsPM100 import ThorlabsPM100

class ThorlabsPowerMeter:
    def __init__(self, resource='USB'):
        rm = visa.ResourceManager()
        self.inst = rm.open_resource(resource)
        self.inst.timeout = None
        self.power_meter = None

    def get_pm(self):
        self.power_meter = ThorlabsPM100(inst=self.inst)
        return self.power_meter