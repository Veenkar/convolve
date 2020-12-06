import wave
import numpy as np
from convlib.audiofile import Audiofile
from logging import getLogger
from logging import DEBUG, INFO, WARN, FATAL

# LOGGER
log = getLogger()

class AudiofileWave(Audiofile):
    def __init__(self, plot_debug):
        super().__init__(plot_debug)

    def _waveload(self, filename):
        with wave.open(filename) as ifile:
            samples = ifile.getnframes()
            audio = ifile.readframes(samples)
            log.debug(f"Loaded {samples} samples from {filename}.")

        # Convert buffer to float32 using NumPy                                                                                 
        audio_as_np_int16 = np.frombuffer(audio, dtype=np.int16)
        audio_as_np_float32 = audio_as_np_int16.astype(np.float64)

        # Normalise float32 array so that values are between -1.0 and +1.0                                                      
        # audio_normalised = audio_as_np_float32 / self.MAX_INT_16
        return audio_as_np_float32

    def _wavesave(self, filename, data, meta):
        log.debug(f"Saving {len(data)} samples to {filename}.")
        self._debug_plt(DEBUG, data)

        audio_as_np_int16 = data.astype(np.int16)
        self._debug_plt(DEBUG, audio_as_np_int16)

        audio_buffer_int16 = audio_as_np_int16.data

        with wave.open(filename, mode='wb') as ofile:
            ofile.setparams(meta)
            ofile.writeframes(audio_buffer_int16)

        self._debug_plt(INFO, audio_buffer_int16)

    def _metaload(self, filename):
        with wave.open(filename) as ifile:
            params = ifile.getparams()
        return params
