#!/usr/bin/python3

import numpy as np
import wave
import argparse
import asyncio

class Convolver:
    def __init__(self, signal, impulse_response):
        self.signal = signal
        self.impulse_response = impulse_response

    def _convolve(self):
        return np.convolve(self.signal, self.impulse_response)

    def convolve(self):
        while True:
            pass

class ConvolverMgr:
    MAX_INT_16 = 2**15
    def __init__(self, input_filename, impulse_filename, output_filename):
        print("in: {}, impulse:{}, out:{}".format(conv_args.input, impulse_filename, output_filename))
        self.input_filename = input_filename
        self.impulse_filename = impulse_filename
        self.output_filename = output_filename

    def _load(self):
        signal = self._waveload(self.input_filename)
        impulse = self._waveload(self.impulse_filename)
        self.convolver = Convolver(signal, impulse)
    
    def _save(self):
        with open(self.output_filename) as w_output:
            # todo save self.output to file
            pass
    async def _convolve_job(self):
        self._load()
        self.output = self.convolver.convolve()
        max_val = np.amax(self.output)
        norm = np.divide(self.MAX_INT_16, max_val)
        self.output = np.divide(self.output, norm)
        print("convolution done")

    def convolve(self):
        try:
            self.tasks = asyncio.run(self._convolve_job())
        except KeyboardInterrupt as e:
            print("Caught keyboard interrupt. Canceling tasks...")

    @staticmethod
    def _wavesave(data):
        pass


    @classmethod
    def _waveload(self, filename):
        with wave.open(filename) as ifile:
            samples = ifile.getnframes()
            audio = ifile.readframes(samples)

        # Convert buffer to float32 using NumPy                                                                                 
        audio_as_np_int16 = np.frombuffer(audio, dtype=np.int16)
        audio_as_np_float32 = audio_as_np_int16.astype(np.float32)

        # Normalise float32 array so that values are between -1.0 and +1.0                                                      
        audio_normalised = audio_as_np_float32 / self.MAX_INT_16
        return audio_normalised

class ConvolverArgumentParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()
        self.add_argument("--input", required=True)
        self.add_argument("--impulse", required=True)
        self.add_argument("--out", required=True)
        self.parse_args()



if __name__ == "__main__":
    conv_parser = ConvolverArgumentParser()
    conv_args = conv_parser.parse_args()
    conv_mgr = ConvolverMgr(conv_args.input, conv_args.impulse, conv_args.out)
    conv_mgr.convolve()

