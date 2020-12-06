import wave
import numpy as np
import logging

# LOGGER
log = logging.getLogger()

class Audiofile:
    def __init__(self, input_filename, impulse_filename, output_filename, plot_debug):
        print("in: {}, impulse:{}, out:{}".format(input_filename, impulse_filename, output_filename))
        self.input_filename = input_filename
        self.impulse_filename = impulse_filename
        self.output_filename = output_filename
        self.plot_debug=plot_debug

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
        self._debug_plt(data)

        audio_as_np_int16 = data.astype(np.int16)
        self._debug_plt(audio_as_np_int16)

        audio_buffer_int16 = audio_as_np_int16.data
        self._debug_plt(audio_buffer_int16)

        with wave.open(filename, mode='wb') as ofile:
            ofile.setparams(meta)
            ofile.writeframes(audio_buffer_int16)

    def _metaload(self, filename):
        with wave.open(filename) as ifile:
            params = ifile.getparams()
        return params

    def _debug_plt(self, plt_data):
        if self.plot_debug:
            ConvolverMgr._plt(plt_data)

    def _plt(self, plt_data):
        time = range(len(plt_data))
        plt.plot(time, plt_data)
        plt.show()
