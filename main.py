import Oscope
import TopticaDLCPro

import high_finesse_ws6.src.high_finesse as hf
from high_finesse_ws6.src.high_finesse import WavelengthMeter
# from IPython.display import clear_output

import pyvisa as visa
from ThorlabsPM100 import ThorlabsPM100

import time
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib as mpl

mpl.rcParams['figure.figsize'] = (10,6)
mpl.rcParams['figure.frameon'] = True
mpl.rcParams['lines.linewidth'] = 2.0
mpl.rcParams['font.size'] = 18
mpl.rcParams['legend.frameon'] = False
mpl.rcParams['legend.fontsize'] = 16


def run():
    # Setup the Toptica laser
    toptica = TopticaDLCPro.TopticaDLCPro(com_port='COM5', baud_rate=115200, timeout=5)
    toptica.set_current(60)

    toptica.enable_current(True)
    toptica.enable_feedforward(enabled=True)
    toptica.set_feedforward(ffwd=-0.49000)

    toptica.set_scan(amplitude=20, offset=10, freq=0.2, shape=1)
    toptica.enable_scan(enabled=False)

    toptica.set_temperature(temp_set=20.20)
    toptica.enable_temp_control(enabled=True)

    # Setup the oscilloscope
    resource_string = 'USB0::0x0AAD::0x010F::100899::INSTR'
    optstr = "AddTermCharToWriteBinBLock=True, TerminationCharacter='\n',AssureWriteWithTermChar=True, WriteDelay=20, ReadDelay=5"

    oscope = Oscope.Oscope(resource_string, optstr)
    oscope.setup_trace(channel='CHAN2', time_scale=0.001, volt_scale=0.02, pos=-2.5)
    # trace = oscope.get_trace(channel='CHAN2', plotting=True)

    # Setup the wavemeter
    wlm = WavelengthMeter(dllpath="C:\\Program Files (x86)\\HighFinesse\\Wavelength Meter WS Ultimate 1653\\Projects\\64\\wlmData.dll")

    rm = visa.ResourceManager()
    # rm.list_resources()
    inst = rm.open_resource('USB0::0x1313::0x8078::P0011560::INSTR')
    power_meter = ThorlabsPM100(inst=inst)
    inst.timeout = None
    power_meter.sense.power.dc.range.auto = "ON"

    currents = np.arange(60, 65, 1)
    max_trace = []
    mean_wlen = []
    act_current = []
    powers = []

    df = pd.DataFrame(columns=['Iset', 'Iact', 'Vmax', 'wlen_mean', 'Power', 'trace'])

    # toptica.set_temperature(temp_set=20.20)
    # toptica.enable_temp_control(enabled=True)
    temp = toptica.get_temperature()

    for i in currents:
        toptica.set_current(int(i))
        time.sleep(5) # The current needs some time to stabilize after being changed
        trace = oscope.get_trace(channel='CHAN2', plotting=False)

        wl = []
        f = []
        t = []
        for j in range(100):
            wl.append(wlm.wavelengths[0])
            f.append(wlm.frequencies[0])
            time.sleep(0.05)
            t.append(i * 0.1)

        # plt.plot(t, wl)
        # plt.show()

        # plt.plot(t, pwr)
        # plt.show()

        power = power_meter.read

        max_trace.append(max(trace))
        mean_wlen.append(np.mean(wl))
        Iact = toptica.get_actual_current()
        act_current.append(Iact)
        powers.append(power)
        print('Set current = {:.2f}'.format(i))
        print('Max FPI voltage = {:.4f} V'.format(max(trace)))
        print('Mean wavelength = {:.4f} nm'.format(np.mean(wl)))
        print('Power = {:.4f} uW'.format(power*1e06))
        print('\n')

        df = df.append(pd.DataFrame(data={'Temp': [temp],
                                'Iset': [i],
                                'Iact': [Iact],
                                'Vmax': max(trace),
                                'wlen_mean': [np.mean(wl)],
                                'Power': [power],
                                'FeedFwd':[ffwd],
                                'trace': [trace],
                                'wavemeter': [wl],
                                't': [t]}))
        df.to_csv('data2.csv')
    # df = pd.DataFrame(data={'Iset':currents,
    #                         'Iact':act_current,
    #                         'Vmax':max_trace,
    #                         'wlen_mean':mean_wlen,
    #                         'Power':powers})
    # df.to_csv('data.csv')


if __name__ == '__main__':
    run()
