import audiofile as af
import numpy as np
from convlib.convaudiofileif import ConvAudiofileIf
from logging import getLogger
from logging import DEBUG, INFO, WARN, FATAL

# LOGGER
log = getLogger()

class ConvAudiofile(ConvAudiofileIf):
    def __init__(self, input_filename, plot_debug):
        super().__init__(plot_debug)
        self._input_filename = input_filename
        self._sample_rate = af.sampling_rate(input_filename)
        self._depth = af.bit_depth(input_filename)

    def waveload(self):
        wave, self.sample_rate = af.read(self._input_filename)
        log.info(f"Loaded {len(wave)} samples from " +
            f"{self._depth}-byte {self._input_filename}. Sample rate: {self._sample_rate}")
        return wave

    def wavesave(self, filename, wave):
        log.info(f"Saving {len(wave)} samples to {filename}. Sample rate: {self._sample_rate}")
        self._debug_plt(INFO, wave)
        af.write(filename, wave, self._sample_rate)
