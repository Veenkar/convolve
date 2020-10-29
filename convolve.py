#!/usr/bin/python3

import numpy
import wave
import argparse

class Convolver:
    def __init__(self, signal, impulse_response):
        self.signal = signal
        self.impulse_response = impulse_response

    def convolve(self):
        return numpy.convolve(signal, impulse_response)

class ConvolverMgr:
    def __init__(self, input_filename, impulse_response_filename, output_filename):
        self.signal_filename = signal_filename
        self.impulse_response_filename = impulse_response_filename

    def _load(self):
        signal = self.waveload(self.signal_filename)
        impulse = w_impulse.read(self.impulse_filename)
        self.convolver = Convolver(signal, impulse)
    
    def convolve(self):
        self._load()
        output = self.convolver.convolve()
        with open(self.output_filename) as w_output:
            w_output.write(output)

    @staticmethod
    def waveload(filename):
        with wave.open("input.wav") as ifile:
            samples = ifile.getnframes()
            audio = ifile.readframes(samples)

        # Convert buffer to float32 using NumPy                                                                                 
        audio_as_np_int16 = numpy.frombuffer(audio, dtype=numpy.int16)
        audio_as_np_float32 = audio_as_np_int16.astype(numpy.float32)

        # Normalise float32 array so that values are between -1.0 and +1.0                                                      
        max_int16 = 2**15
        audio_normalised = audio_as_np_float32 / max_int16
        return audio_normalised

class ConvolverArgumentParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()
        self.add_argument("--input", required=True, nargs=1)
        self.add_argument("--impulse", required=True, nargs=1)
        self.add_argument("--out", required=True, nargs=1)
        self.parse_args()



if __name__ == "__main__":
    conv_parser = ConvolverArgumentParser()
    conv_args = conv_parser.parse_args()
    print("in: {}, impulse:{}, out:{}".format(conv_args.input, conv_args.impulse, conv_args.out))
    conv_mgr = ConvolverMgr("input.wav", "impulse.wav")
    conv_mgr.main()

