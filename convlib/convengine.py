import logging
import numpy as np

# LOGGER
log = logging.getLogger()

class Convengine:
    MAX_OUT_VAL = 0.99
    
    def __init__(self, signal, impulse_response):
        self.signal = signal
        self.impulse_response = impulse_response

    def _convolve(self):
        output  = np.convolve(self.signal, self.impulse_response, mode="same")
        max_val = np.max(np.abs(output), axis=0)
        norm    = float(self.MAX_OUT_VAL) / max_val
        output  = np.multiply(output, norm)
        return output

    def convolve(self):
        return self._convolve()
