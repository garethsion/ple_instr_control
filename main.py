import Oscope
import TopticaDLCPro

import high_finesse_ws6.src.high_finesse as hf
from high_finesse_ws6.src.high_finesse import WavelengthMeter
# from IPython.display import clear_output

import time
import numpy as np
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
    trace = oscope.get_trace(channel='CHAN2', plotting=True)

    # Setup the wavemeter
    wlm = WavelengthMeter(dllpath="C:\\Program Files (x86)\\HighFinesse\\Wavelength Meter WS Ultimate 1653\\Projects\\64\\wlmData.dll")

    wl = []
    f = []
    t = []
    for i in range(100):
        wl.append(wlm.wavelengths[0])
        f.append(wlm.frequencies[0])
        time.sleep(0.05)
        t.append(i * 0.1)

    plt.plot(t, wl)
    plt.show()

    # plt.plot(t, pwr)
    # plt.show()

    print('Max FPI voltage = {:.4f} V'.format(max(trace)))
    print('Mean wavelength = {:.4f} nm'.format(np.mean(wl)))


if __name__ == '__main__':
    run()
