import logging
import numpy as np

# LOGGER
log = logging.getLogger()

class Convengine:
    MAX_OUT_VAL = 0.99
    
    def __init__(self, signal, impulse):
        self.signal = signal
        self.impulse = impulse

    def _convolve(self, signal, impulse):
        output  = np.convolve(signal, np.array(impulse), mode="same")
        max_val = np.max(np.abs(output), axis=0)
        norm    = float(self.MAX_OUT_VAL) / max_val
        output  = np.multiply(output, norm)
        return output

    def _duplicate_wave_to_channels(self, wave, num_channels):
        wave_arr = [wave for x in range(num_channels)]
        return np.array(wave_arr)

    def convolve(self):
        sig_dim = len(self.signal.shape)
        imp_dim = len(self.impulse.shape)

        if sig_dim > imp_dim:
            self.impulse = self._duplicate_wave_to_channels(self.impulse, 2)
        elif sig_dim < imp_dim:
            self.signal = self._duplicate_wave_to_channels(self.signal, 2)

        convolved_arr = [self._convolve(self.signal[x], self.impulse[x]) for x in range(2)]

        return np.array(convolved_arr)
