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

    def _dtype(self, num_bytes):
        dtype_arr = [ (f'f{x}', np.uint8) for x in range(num_bytes) ]
        return np.dtype(dtype_arr)

    # TODO: check performance
    def _int(self, byte_tuple, big_endian):
        if big_endian:
            byte_arr = [x for x in byte_tuple]
        else:
            byte_arr = [x for x in reversed(byte_tuple)]

        subtrahend_bit = byte_arr[0] & 0x80
        shift_count = 8 * (len(byte_arr) -1)
        subtrahend = subtrahend_bit << shift_count
        minuend = (byte_arr[0] & 0x7F)
        for el in byte_arr[1:]:
            minuend = minuend << 8
            minuend += el
        return int(minuend) - subtrahend

    def _frombuffer(self, buffer, sample_width, big_endian):
        uintx_dtype = self._dtype(sample_width)
        audio_as_uintx_dtype = np.frombuffer(buffer, dtype=uintx_dtype)
        return np.array([self._int(x, big_endian) for x in audio_as_uintx_dtype])

    def _waveload(self, filename):
        with wave.open(filename) as ifile:
            samples = ifile.getnframes()
            audio = ifile.readframes(samples)
            params = ifile.getparams()
            sample_width = params.sampwidth
            log.info(f"Loaded {samples} samples from {sample_width}-byte {filename}.")
        
        # Convert buffer to float32 using NumPy
        if sample_width == 2:
            audio_as_np_int16 = np.frombuffer(audio, dtype=np.int16)
            audio_as_np_float = audio_as_np_int16.astype(np.float64)
        elif sample_width == 4:
            audio_as_np_int16 = np.frombuffer(audio, dtype=np.int32)
            audio_as_np_float = audio_as_np_int16.astype(np.float64)
        else:
            log.warn("24-bit wave detected. Slower conversion due to lack of 24-bit int support in numpy.")
            audio_arr = self._frombuffer(audio, sample_width, big_endian=False)
            audio_as_np_float = np.array(audio_arr)

        # Normalise float32 array so that values are between -1.0 and +1.0                                                      
        # audio_normalised = audio_as_np_float32 / self.MAX_INT_16
        return audio_as_np_float

    def _wavesave(self, filename, data, meta):
        meta = meta._replace(sampwidth = 2)

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
