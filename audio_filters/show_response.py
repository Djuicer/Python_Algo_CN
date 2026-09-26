"""
绘制音频滤波器的幅频响应和相频响应。

https://en.wikipedia.org/wiki/Frequency_response
"""

from __future__ import annotations

from abc import abstractmethod
from math import pi
from typing import Protocol

import matplotlib.pyplot as plt
import numpy as np


class FilterType(Protocol):
    @abstractmethod
    def process(self, sample: float) -> float:
        """
        计算 y[n]。

        >>> issubclass(FilterType, Protocol)
        True
        """


def get_bounds(
    fft_results: np.ndarray, samplerate: int
) -> tuple[int | float, int | float]:
    """
    获取显示 FFT 结果时使用的边界。

    >>> import numpy
    >>> array = numpy.linspace(-20.0, 20.0, 1000)
    >>> get_bounds(array, 1000)
    (-20, 20)
    """
    lowest = min([-20, np.min(fft_results[1 : samplerate // 2 - 1])])
    highest = max([20, np.max(fft_results[1 : samplerate // 2 - 1])])
    return lowest, highest


def show_frequency_response(filter_type: FilterType, samplerate: int) -> None:
    """
    显示滤波器的频率响应。

    >>> from audio_filters.iir_filter import IIRFilter
    >>> filt = IIRFilter(4)
    >>> show_frequency_response(filt, 48000)
    """

    size = 512
    inputs = [1] + [0] * (size - 1)
    outputs = [filter_type.process(item) for item in inputs]

    filler = [0] * (samplerate - size)  # 补零
    outputs += filler
    fft_out = np.abs(np.fft.fft(outputs))
    fft_db = 20 * np.log10(fft_out)

    # 从 24 Hz 到奈奎斯特频率采用对数刻度
    plt.xlim(24, samplerate / 2 - 1)
    plt.xlabel("Frequency (Hz)")
    plt.xscale("log")

    # 在合理的边界内显示
    bounds = get_bounds(fft_db, samplerate)
    plt.ylim(max([-80, bounds[0]]), min([80, bounds[1]]))
    plt.ylabel("Gain (dB)")

    plt.plot(fft_db)
    plt.show()


def show_phase_response(filter_type: FilterType, samplerate: int) -> None:
    """
    显示滤波器的相位响应。

    >>> from audio_filters.iir_filter import IIRFilter
    >>> filt = IIRFilter(4)
    >>> show_phase_response(filt, 48000)
    """

    size = 512
    inputs = [1] + [0] * (size - 1)
    outputs = [filter_type.process(item) for item in inputs]

    filler = [0] * (samplerate - size)  # 补零
    outputs += filler
    fft_out = np.angle(np.fft.fft(outputs))

    # 从 24 Hz 到奈奎斯特频率采用对数刻度
    plt.xlim(24, samplerate / 2 - 1)
    plt.xlabel("Frequency (Hz)")
    plt.xscale("log")

    plt.ylim(-2 * pi, 2 * pi)
    plt.ylabel("Phase shift (Radians)")
    plt.plot(np.unwrap(fft_out, -2 * pi))
    plt.show()
