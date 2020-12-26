import audiofile as af
import numpy as np
from convlib.convaudiofileif import ConvAudiofileIf
from logging import getLogger
from logging import DEBUG, INFO, WARN, FATAL

# LOGGER
log = getLogger()

class ConvAudiofile(ConvAudiofileIf):
    def __init__(self, input_filename, plot_debug):
        super().__init__(input_filename, plot_debug)
        self._sample_rate = af.sampling_rate(input_filename)
        self._depth = af.bit_depth(input_filename)

    def waveload(self):
        wave, self.sample_rate = af.read(self._input_filename)
        log.info(f"Loaded {wave.shape} samples from " +
            f"{self._depth}-byte {self._input_filename}. Sample rate: {self._sample_rate}")
        return wave

    def wavesave(self, filename, wave):
        log.info(f"Saving {wave.shape} samples to {filename}. Sample rate: {self._sample_rate}")
        self.ensure_dirs(filename)
        self.debug_plt(INFO, wave)
        af.write(str(filename), wave, self._sample_rate)
