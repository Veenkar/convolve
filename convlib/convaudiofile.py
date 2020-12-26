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
        samples, self.sample_rate = af.read(filename)
        log.info(f"Loaded {len(samples)} samples from {self.sample_rate}-byte {filename}. Sample rate: {self.sample_rate}")
        return samples

    def wavesave(self, filename, data):
        log.info(f"Saving {len(data)} samples to {filename}. Sample rate: {self._sample_rate}")
        self._debug_plt(INFO, data)
        af.write(filename, data, self.sample_rate)
