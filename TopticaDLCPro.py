import sys

import matplotlib.pyplot as pyplot

from toptica.lasersdk.dlcpro.v2_0_3 import DLCpro, SerialConnection, DeviceNotFoundError
from toptica.lasersdk.utils.dlcpro import *

import numpy as np
from contextlib import contextmanager


class TopticaDLCPro:

    def __init__(self, com_port, baud_rate, timeout):
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.dlc = DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout))

    # def __enter__(self):
    #     print('Entered')
    #     return self.dlc
    #
    # def __exit__(self, type, value, traceback):
    #     print('Exit')
    #     return

    # @contextmanager
    # def dlc(self):
    #     self.dlc = DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout))
    #     yield self.dlc
    #     print('Yay')

    def set_current(self, set_current):
        with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
            dlc.laser1.dl.cc.current_set.set(set_current)
        # self.dlc.laser1.dl.cc.current_set(set_current)

    def get_actual_current(self):
        with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
            return dlc.laser1.dl.cc.current_act.get()

    def enable_current(self, enabled=True):
        with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
            dlc.laser1.dl.cc.enabled.set(enabled)
            print('Current emission enabled' if enabled else 'Current emission disabled')

    def enable_feedforward(self, enabled=True):
        with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
            dlc.laser1.dl.cc.feedforward_enabled.set(enabled)
            print('Feedforward enabled' if enabled else 'Feedforward disabled')

    def set_feedforward(self, ffwd):
        with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
            dlc.laser1.dl.cc.feedforward_factor.set(ffwd)

    def set_scan(self, amplitude=20, offset=10, freq=0.4, shape=1):
        with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
            dlc.laser1.scan.amplitude.set(amplitude)
            dlc.laser1.scan.offset.set(offset)
            dlc.laser1.scan.frequency.set(freq)
            dlc.laser1.scan.signal_type.set(shape)  # 0:sine, 1:Triangle, 2:Sawtooth

    def enable_scan(self, enabled=True):
        with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
            dlc.laser1.scan.enabled.set(enabled)
            print('Scan enabled' if enabled else 'Scan disabled')

    def set_temperature(self, temp_set=20.2):
        with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
            dlc.laser1.dl.tc.temp_set.set(temp_set)

    def get_temperature(self):
        with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
            return dlc.laser1.dl.tc.temp_act.get()

    def get_feedforward(self):
        with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
            return dlc.laser1.dl.cc.feedforward_factor.get()

    def enable_temp_control(self, enabled=True):
        with DLCpro(SerialConnection(self.com_port, self.baud_rate, self.timeout)) as dlc:
            dlc.laser1.dl.tc.enabled.set(enabled)
            print('Temp control enabled' if enabled else 'Temp control disabled')