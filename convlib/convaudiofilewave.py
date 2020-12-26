import wave
import audiofile as af
import numpy as np
from convlib.convaudiofileif import ConvAudiofileIf
from logging import getLogger
from logging import DEBUG, INFO, WARN, FATAL

# LOGGER
log = getLogger()

class ConvAudiofileWave(ConvAudiofileIf):
    def __init__(self, plot_debug):
        super().__init__(plot_debug)
        self.sample_rate = None

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

    def waveload(self, filename):
        samples, self.sample_rate = af.read(filename)
        return samples

    def wavesave(self, filename, data, sample_rate):
        log.debug(f"Saving {len(data)} samples to {filename}.")
        self._debug_plt(DEBUG, data)

        audio_as_np_int16 = data.astype(np.int16)
        self._debug_plt(DEBUG, audio_as_np_int16)

        audio_buffer_int16 = audio_as_np_int16.data

        with wave.open(filename, mode='wb') as ofile:
            ofile.setnchannels(1)
            ofile.setsampwidth(2)
            ofile.setframerate(sample_rate)
            ofile.writeframes(audio_buffer_int16)

        self._debug_plt(INFO, audio_buffer_int16)

    def _metaload(self, filename):
        if not self.sample_rate:
            raise(Exception("Use waveload first!"))
        return self.sample_rate

