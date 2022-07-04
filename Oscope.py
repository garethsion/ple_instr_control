"""Class to communicate with the Rohde&Schwarz RTM Oscilloscope.
"""

from RsInstrument.RsInstrument import RsInstrument
import time

from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = (10, 6)
mpl.rcParams['figure.frameon'] = True
mpl.rcParams['lines.linewidth'] = 2.0
mpl.rcParams['font.size'] = 18
mpl.rcParams['legend.frameon'] = False
mpl.rcParams['legend.fontsize'] = 16


class Oscope:
    """Communicate with a Rohde & Schwarz RTM Oscilloscope.

    Author      : Gareth Sion Jones
    Affiliation : University of Oxford
    Date        : July, 2022

    Example:
        >>> oscope = Oscope.Oscope(resource_string, optstr) # Instantiate object with eresource string and options string
        >>> oscope.setup_trace(channel='CHAN1', time_scale=0.001, volt_scale=0.02, pos=-2.5) # setup oscope trace
        >>> trace = oscope.get_trace(channel='CHAN1', plotting=True) # return trace data

    """

    def __init__(self, resource_string='USB', optstr=''):
        """Initialize the oscilloscope

        :param resource_string : name of com port resource
        :param optstr : string of options to pass to the RSInstrument
        """
        self.instr = RsInstrument(resource_string, True, True, optstr)
        self.instr.timeout = 3000
        self.instr.write_str("CHAN1:STAT OFF")
        self.instr.write_str("CHAN2:STAT OFF")
        self.instr.write_str("CHAN3:STAT OFF")
        self.instr.write_str("CHAN4:STAT OFF")

    def __call__(self):
        idn = self.instr.query_str('*IDN?')
        print(f"\nHello, I am: '{idn}'")
        print(f'RsInstrument driver version: {self.instr.driver_version}')
        print(f'Visa manufacturer: {self.instr.visa_manufacturer}')
        print(f'Instrument full name: {self.instr.full_instrument_model_name}')
        print(f'Instrument installed options: {",".join(self.instr.instrument_options)}')

    def setup_trace(self, channel='CHAN1', time_scale=0.1, volt_scale=0.1, pos=2.5):
        self.instr.write_str("*RST")  # Reset the instrument, clear the Error queue
        self.instr.write_str(channel + ":STAT ON")
        self.instr.write_str(channel + ":SCAL " + str(volt_scale))

        # basic settings - to test with RTH probe compensation signal
        self.instr.write_str("TIM:SCAL " + str(time_scale))
        self.instr.write_str(channel + ":POS " + str(pos))

        self.instr.write_str('TRIG:A:MODE AUTO')
        self.instr.write_str('TRIG:A:SOUR ' + channel.replace('AN', ''))
        self.instr.write_str("TRIG:A:TYPE EDGE;:TRIG:A:EDGE:SLOP POS")  # Trigger type Edge Positive
        # instr.write_str("TRIG:A:LEV 0.06")  # Trigger level 40mV
        self.instr.write_str('TRIG:A:FIND')
        self.instr.query_opc()  # Using *OPC? query waits until all the instrument settings are finished

        start = time.time()
        self.instr.write_str_with_opc("RUN")
        stop = time.time()
        print('RTH triggered, capturing data ...')
        print(f'Number of sample points: {self.instr.query_float("ACQ:POIN?")}')
        print(f'Data capturing elapsed time: {stop - start:.3f}sec')

        # get binary data
        start = time.time()
        self.instr.data_chunk_size = 100000  # transfer in blocks of 100k bytes (default)
        time.sleep(2)

        ch_scale = self.instr.query_float(channel + ":SCAL?")
        ch_offs = self.instr.query_float(channel + ":OFFS?")
        ch_pos = self.instr.query_float(channel + ":POS?")

        # see RTH manual for details -> Transfer of Waveform Data
        factor = ch_scale * 8 / (255 * 256)
        offs = ch_offs - ch_pos * ch_scale

    def get_trace(self, channel='CHAN1', plotting=True):
        # get ASCII data
        start = time.time()
        self.instr.write_str("FORM:DATA ASC")
        self.instr.data_chunk_size = 100000  # transfer in blocks of 100k bytes (default)
        data_asc = self.instr.query_bin_or_ascii_float_list(channel + ":DATA?")

        print(f'ASCII waveform transfer elapsed time: {time.time() - start:.3f}sec')
        if plotting:
            plt.figure(1)
            plt.plot(data_asc, 'k')
            plt.title('Oscope Output')
            plt.xlabel('Samples')
            plt.ylabel('Voltage (V)')
            plt.show()
        return data_asc

    def close_instr(self):
        # Close the session
        self.instr.close()
