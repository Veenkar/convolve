
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from logging import getLogger
from pathlib import Path

# LOGGER
log = getLogger()


class ConvAudiofileIf(ABC):
    def __init__(self, input_filename, plot_debug):
        print(f"plot debug: {plot_debug}")
        self._input_filename = input_filename
        self.plot_debug = plot_debug
        self._sample_rate = None

    @property
    def input_filename(self):
        return self._input_filename

    @property
    def sample_rate(self):
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, val):
        self._sample_rate = val

    @abstractmethod
    def waveload(self, filename):
        pass

    @abstractmethod
    def wavesave(self, filename, data, meta):
        pass

    def ensure_dirs(self, filename):
        output_path = Path(filename)
        output_parent_tuple = output_path.parts[:-1]
        output_parent_path = Path(*output_parent_tuple)
        output_parent_path.mkdir(parents=True, exist_ok=True)

    def _debug_plt(self, level, plt_data):
        if level >= self.plot_debug:
            self._plt(plt_data)

    def _plt(self, plt_data):
        time = range(len(plt_data))
        plt.plot(time, plt_data)
        plt.show()

    def debug_plt(self, level, plt_data):
        if len(plt_data.shape) <= 1:
            self._debug_plt(level, plt_data)
        else:
            for chan_data in plt_data:
                self._debug_plt(level, chan_data)



