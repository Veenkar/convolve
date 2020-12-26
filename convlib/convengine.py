import logging
import numpy as np

# LOGGER
log = logging.getLogger()

class Convengine:
    MAX_OUT_VAL = 0.99
    
    def __init__(self, impulse):
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

    def convolve(self, signal):
        sig_dim = len(signal.shape)
        imp_dim = len(self.impulse.shape)
        impulse = self.impulse

        if sig_dim > imp_dim:
            impulse = self._duplicate_wave_to_channels(self.impulse, 2)
        elif sig_dim < imp_dim:
            signal = self._duplicate_wave_to_channels(signal, 2)

        if sig_dim > 1:
            convolved_arr = [self._convolve(signal[x], impulse[x]) for x in range(2)]
        else:
            convolved_arr = self._convolve(signal, impulse)

        return np.array(convolved_arr)
