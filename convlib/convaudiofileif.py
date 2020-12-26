
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from logging import getLogger

# LOGGER
log = getLogger()


class ConvAudiofileIf(ABC):
    def __init__(self, plot_debug):
        print(f"plot debug: {plot_debug}")
        self.plot_debug = plot_debug
        self._sample_rate = None

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

    def _debug_plt(self, level, plt_data):
        if level >= self.plot_debug:
            self._plt(plt_data)

    def _plt(self, plt_data):
        time = range(len(plt_data))
        plt.plot(time, plt_data)
        plt.show()

