import numpy as np

from enum import Enum
from scipy.io import loadmat
from dataclasses import dataclass


class Flank(Enum):
    rising = 0
    falling = 1


@dataclass
class Data:
    vm: np.array
    am: np.array
    amfs: float
    eod: np.array
    eod_times : np.array
    fs: float
    dp: np.array
    dpfs: float
    comment_times: np.array

    @property
    def time(self):
        return np.arange(len(self.vm)) / self.fs
    @property
    def dipole_time(self):
        return np.arange(len(self.vm)) / self.fs
    @property
    def am_time(self):
        return np.arange(len(self.am)) / self.amfs



def load_data(filename):
    data = loadmat(filename, squeeze_me=True, simplify_cells=True)
    eod = data["Ch1"]["values"]
    eod_times = data["Ch2"]["times"]
    vm = data["Ch5"]["values"]
    am = data["Ch3"]["values"]
    amfs = 1./data["Ch3"]["interval"]
    fs = 1./data["Ch5"]["interval"]
    dp = data["Ch6"]["values"]
    dpfs = data["Ch6"]["interval"]
    ct = data["Ch31"]["times"]
    d = Data(vm, am, amfs, eod, eod_times, fs, dp, dpfs, ct)
    return d


def threshold_crossing(data, time, threshold=0.0, flank=Flank.rising):
    if flank == Flank.rising:
        indices = np.where((data > threshold) & (np.roll(data, 1) <= threshold))[0]
    else:
        indices = np.where((data <= threshold) & (np.roll(data, 1) > threshold))[0]
    times = time[indices]
    return times, indices