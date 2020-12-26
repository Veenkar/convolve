import audiofile as af
import numpy as np
from convlib.convaudiofileif import ConvAudiofileIf
from logging import getLogger
from logging import DEBUG, INFO, WARN, FATAL

# LOGGER
log = getLogger()

class ConvAudiofile(ConvAudiofileIf):
    def __init__(self, plot_debug):
        super().__init__(plot_debug)
        self.sample_rate = None

    def waveload(self, filename):
        wave, self.sample_rate = af.read(filename)
        self.depth = af.bit_depth(filename)
        log.info(f"Loaded {len(wave)} samples from " +
            f"{self.depth}-byte {filename}. Sample rate: {self.sample_rate}")
        return wave

    def wavesave(self, filename, wave):
        log.info(f"Saving {len(wave)} samples to {filename}. Sample rate: {self._sample_rate}")
        self._debug_plt(INFO, wave)
        af.write(filename, wave, self.sample_rate)
