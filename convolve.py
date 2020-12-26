#!/usr/bin/python3

from convlib.convaudiofile import ConvAudiofile
from convlib.convengine import Convengine
from convlib.convarg import Convarg

from pathlib import Path

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
    class NoAudiofilesFoundException(Exception):
        def __init__(self, dirname):
            msg = ""
            msg += f"No audiofiles found in {dirname}"
            msg += f" or {dirname} is not a directory!"
            super().__init__(msg)

    def __init__(self, signal_filename, impulse_filename, output_filename, recursive=False, plot_debug=logging.WARN):
        print("in: {}, impulse:{}, out:{}, recursive:{}" \
            .format(signal_filename, impulse_filename, output_filename, recursive))
        self.signal_filenames = self.resolve_inputs(signal_filename, recursive)
        self.impulse_filename = impulse_filename
        self.output_filename = output_filename
        self.recursive = recursive

        self.impulse_audiofile = ConvAudiofile(self.impulse_filename, plot_debug=plot_debug)

        self.signal_audiofiles = []
        for signal_filename in self.signal_filenames:
            signal_audiofile = ConvAudiofile(signal_filename, plot_debug=plot_debug)
            self.signal_audiofiles.append(signal_audiofile)

            if self.impulse_audiofile.sample_rate != signal_audiofile.sample_rate:
                raise Exception("Sample rates must match!")

        pass

    def resolve_inputs(self, signal_filename, recursive):
        if recursive:
            path = Path(signal_filename)
            res = [ str(x) for x in path.glob('**/*')]
        else:
            res = [ signal_filename ]

        if len(res) <= 0:
            raise( self.NoAudiofilesFoundException(signal_filename))

        return res

    def convolve(self):
        impulse_data = self._load_impulse()
        self.convolver = Convengine(impulse_data)

        if len(self.signal_audiofiles) > 1:
            for sig in self.signal_audiofiles:
                output_branch_tuple = Path(sig.input_filename).parts[1:]
                output_path = Path(self.output_filename) / Path(*output_branch_tuple)

                output_filename = str(output_path)
                self._run_convolve_job(sig, output_filename)
        else:
            self._run_convolve_job(self.signal_audiofiles[0], self.output_filename)

        #for signal_audiofile in self.signal_audiofiles:
        #    self._run_convolve_job(signal_audiofile, output_filename)

    def _run_convolve_job(self, wave, output_filename):
        try:
            self.tasks = asyncio.run(self._convolve_job(wave, output_filename))
        except KeyboardInterrupt as e:
            print("Caught keyboard interrupt. Canceling tasks...")  

    async def _convolve_job(self, audiofile, output_filename):
        wave = audiofile.waveload()
        output = self.convolver.convolve(wave)
        self._save(output, output_filename)
        print("convolution done")

    def _load_impulse(self):
        return self.impulse_audiofile.waveload()
    
    def _save(self, output, output_filename):
        self.impulse_audiofile.wavesave(output_filename, output)


if __name__ == "__main__":
    conv_parser = Convarg()
    conv_args = conv_parser.parse_args()
    conv_mgr = ConvolverMgr(
        conv_args.input, conv_args.impulse, conv_args.out,
        recursive=conv_args.recursive, plot_debug=PLOT_DEBUG
    )
    conv_mgr.convolve()

