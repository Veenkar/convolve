#!/usr/bin/python3

from convlib.convaudiofile import ConvAudiofile
from convlib.convengine import Convengine
from convlib.convarg import Convarg

import numpy as np
import argparse
import asyncio
import logging
import sys

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
PLOT_DEBUG = logging.INFO

# LOGGER
log = logging.getLogger()
log.setLevel(logging.INFO)
sh = logging.StreamHandler(sys.stdout)
log.addHandler(sh)



class ConvolverMgr():
    def __init__(self, input_filename, impulse_filename, output_filename, recursive=False, plot_debug=logging.WARN):
        print("in: {}, impulse:{}, out:{}, recursive:{}" \
            .format(input_filename, impulse_filename, output_filename, recursive))
        self.input_filename = input_filename
        self.impulse_filename = impulse_filename
        self.output_filename = output_filename
        self.recursive = recursive

        self.impulse_audiofile = ConvAudiofile(self.impulse_filename, plot_debug=plot_debug)
        self.signal_audiofile = ConvAudiofile(self.input_filename, plot_debug=plot_debug)

        if self.impulse_audiofile.sample_rate != self.signal_audiofile.sample_rate:
            raise Exception("Sample rates must match!")

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
        impulse = self.impulse_audiofile.waveload()
        signal = self.signal_audiofile.waveload()

        self.convolver = Convengine(signal, impulse)
    
    def _save(self):
        self.impulse_audiofile.wavesave(self.output_filename, self.output)


if __name__ == "__main__":
    conv_parser = Convarg()
    conv_args = conv_parser.parse_args()
    conv_mgr = ConvolverMgr(
        conv_args.input, conv_args.impulse, conv_args.out,
        recursive=conv_args.recursive, plot_debug=PLOT_DEBUG
    )
    conv_mgr.convolve()

