#!/usr/bin/python3

import numpy as np
import argparse
import asyncio
import matplotlib.pyplot as plt
import logging
import sys
from convlib.audiofile import Audiofile

# TODO
# allow for using any wav file format (16,24,32 bit), use this:
# https://stackoverflow.com/questions/34009653/convert-bytes-to-int
# output format should be same as input
#
# allow correct processing of channels
# > 2ch in, 2ch impulse -> 2ch stereo output,
#   channel 1 convolved with channel 1, ch 2 with ch 2
# > 2ch in, 1ch impulse -> 2ch stereo output,
#   both channels of input convolved with impulse
# > 1ch in, 2ch impulse -> same


# CONFIG
PLOT_DEBUG = False

# LOGGER
log = logging.getLogger()
log.setLevel(logging.DEBUG)
sh = logging.StreamHandler(sys.stdout)
log.addHandler(sh)

class Convolver:
    MAX_INT_16 = (2**15)-1
    MAX_OUTPUT_FACTOR = 0.99
    MAX_OUT_VAL = int(MAX_OUTPUT_FACTOR * MAX_INT_16)
    
    def __init__(self, signal, impulse_response):
        self.signal = signal
        self.impulse_response = impulse_response

    def _convolve(self):
        output  = np.convolve(self.signal, self.impulse_response, mode="same")
        max_val = np.max(np.abs(output), axis=0)
        norm    = float(self.MAX_OUT_VAL) / max_val
        output  = np.multiply(output, norm)
        return output

    def convolve(self):
        return self._convolve()

class ConvolverMgr(Audiofile):
    def __init__(self, input_filename, impulse_filename, output_filename, plot_debug=False):
        super().__init__(input_filename, impulse_filename, output_filename, plot_debug)

    def convolve(self):
        try:
            self.tasks = asyncio.run(self._convolve_job())
        except KeyboardInterrupt as e:
            print("Caught keyboard interrupt. Canceling tasks...")  

    async def _convolve_job(self):
        self._load()
        self.output = self.convolver.convolve()
        self._save()
        print("convolution done")

    def _load(self):
        signal = self._waveload(self.input_filename)
        impulse = self._waveload(self.impulse_filename)
        self.meta = self._metaload(self.input_filename)
        self.convolver = Convolver(signal, impulse)
    
    def _save(self):
        self._wavesave(self.output_filename, self.output, self.meta)



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
    conv_mgr = ConvolverMgr(
        conv_args.input, conv_args.impulse, conv_args.out, plot_debug=PLOT_DEBUG
    )
    conv_mgr.convolve()

