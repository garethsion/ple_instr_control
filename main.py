import Oscope
import TopticaDLCPro
import ThorlabsPowerMeter as pm
from high_finesse_ws6.src.high_finesse import WavelengthMeter

import datetime as dt
import time
import numpy as np
import pandas as pd


def run():
    # Connect the Toptica laser
    toptica = TopticaDLCPro.TopticaDLCPro(com_port='COM5', baud_rate=115200, timeout=5)

    # Connect the oscilloscope
    resource_string = 'USB0::0x0AAD::0x010F::100899::INSTR'
    optstr = "AddTermCharToWriteBinBLock=True, TerminationCharacter='\n',AssureWriteWithTermChar=True, WriteDelay=20, ReadDelay=5"

    oscope = Oscope.Oscope(resource_string, optstr)
    oscope.setup_trace(channel='CHAN2', time_scale=0.1, volt_scale=0.08, pos=0)

    # Connect the wavemeter
    wlm = WavelengthMeter(dllpath="C:\\Program Files (x86)\\HighFinesse\\Wavelength Meter WS Ultimate 1653\\Projects\\64\\wlmData.dll")

    # Connect the power meter
    pmt = pm.ThorlabsPowerMeter(resource='USB0::0x1313::0x8078::P0011560::INSTR')
    power_meter = pmt.get_pm()
    power_meter.sense.power.dc.range.auto = "ON"

    # Initial setup of Toptica DLC Pro
    toptica.set_current(55)
    toptica.enable_current(True)
    toptica.enable_feedforward(enabled=True)
    toptica.set_feedforward(ffwd=-0.49000)
    toptica.set_scan(amplitude=20, offset=10, freq=0.2, shape=1)
    toptica.enable_scan(enabled=True)
    toptica.enable_temp_control(enabled=True)

    # Define iterables
    temperatures = np.arange(16, 26, 2)
    currents = np.arange(63, 148, 1)
    feedfwrds = np.arange(-0.9, 0, 0.01)
    scan_volts = np.arange(10, 35, 1)
    scan_offs = np.arange(10, 90, 1)

    # Dataframe for collecting all data from sweep
    df = pd.DataFrame(columns=['Iset', 'Iact', 'Vmax', 'wlen_mean', 'Power', 'trace'])

    for temp in temperatures:
        toptica.set_temperature(temp)
        actual_temp = toptica.get_temperature()
        time.sleep(2400)  # Wait four minutes for temperature to stabilize.
        for sv in scan_volts:
            for so in scan_offs:
                toptica.set_scan(amplitude=sv, offset=so, freq=0.2, shape=1)
                for i in currents:
                    toptica.set_current(int(i))
                    Iact = toptica.get_actual_current()
                    for ffwd in feedfwrds:
                        toptica.set_feedforward(ffwd)
                        time.sleep(5)  # The current needs some time to stabilize after being changed
                        trace = oscope.get_trace(channel='CHAN2', plotting=False)

                        wl = []  # wavelengths from wavemeter
                        wlm_pwrs = []  # powers from wavemeter
                        f = []  # frequencies from wavemeter
                        t = []  # time from wavemeter
                        pwr_met = []  # power from Thorlabs power meter
                        for j in range(300):
                            wl.append(wlm.wavelengths[0])
                            f.append(wlm.frequencies[0])
                            wlm_pwrs.append(wlm.powers[0])
                            time.sleep(0.05)
                            t.append(i * 0.1)
                            pwr_met.append(power_meter.read)

                        print('Set temperature = {:.4f} C'.format(max(trace)))
                        print('Set scan voltage = {:.2f} V'.format(sv))
                        print('Set scan offset = {:.2f} V'.format(so))
                        print('Set current = {:.2f} mA'.format(i))
                        print('Set feedforward = {:.2f}'.format(ffwd))
                        print('\n')

                        df = df.append(pd.DataFrame(data={'temp_set': [temp],
                                                          'temp_act': [actual_temp]
                                                          'scan_voltage': [sv],
                                                          'scan_offset': [so],
                                                          'Iset': [i],
                                                          'Iact':  [Iact]
                                                          'power_meter': [pwr_met],
                                                          'feedfwd':[ffwd],
                                                          'trace': [trace],
                                                          'wavemeter': [wl],
                                                          'wavemeter_power': [wlm_pwrs],
                                                          't': [t],
                                                          'datetime': dt.datetime.now()}))
                        df.to_csv('full_toptica_sweep.csv')
    toptica.set_current(60)
    toptica.enable_current(enabled=False)
    toptica.set_temperature(20)

    # df = pd.DataFrame(data={'Iset':currents,
    #                         'Iact':act_current,
    #                         'Vmax':max_trace,
    #                         'wlen_mean':mean_wlen,
    #                         'Power':powers})
    # df.to_csv('data.csv')


if __name__ == '__main__':
    run()
