from __future__ import annotations

from json import loads
from pathlib import Path

import numpy as np
from scipy.linalg import toeplitz
from scipy.signal import lfilter, unit_impulse

from audio_filters.butterworth_filter import make_highpass
from audio_filters.iir_filter import IIRFilter

data = loads((Path(__file__).resolve().parent / "loudness_curve.json").read_text())


def _polystab(poly: np.ndarray) -> np.ndarray:
    """
    将单位圆外的所有根反射到圆内，以使多项式稳定。这样可在不改变
    幅频响应的情况下保持所得 IIR 滤波器的稳定性。

    https://en.wikipedia.org/wiki/Minimum_phase

    >>> np.round(_polystab(np.array([1.0, 2.0, 1.0])), 6)
    array([1., 2., 1.])
    >>> np.round(_polystab(np.array([1.0, 2.0, 1.01])), 6)
    array([1.      , 1.980198, 0.990099])
    """
    if poly.size <= 1:
        return poly
    roots = np.roots(poly)
    nonzero = np.where(roots != 0)[0]
    outside = 0.5 * (np.sign(np.abs(roots[nonzero]) - 1) + 1)
    roots[nonzero] = (1 - outside) * roots[nonzero] + outside / np.conj(roots[nonzero])
    stabilized = np.poly(roots)
    if not np.imag(poly).any():
        stabilized = np.real(stabilized)
    return stabilized


def _numerator(
    impulse_response: np.ndarray, denominator: np.ndarray, numerator_order: int
) -> np.ndarray:
    """
    给定传递函数的脉冲响应和已知分母多项式，使用最小二乘法估计
    其分子多项式。

    >>> num = _numerator(np.array([1.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0]), 1)
    >>> np.round(num, 6)
    array([1., 0.])
    """
    length = impulse_response.size
    impulse = lfilter([1.0], denominator.ravel(), unit_impulse(length))
    toep = toeplitz(impulse, unit_impulse(numerator_order + 1))
    return np.linalg.lstsq(toep.conj(), impulse_response.ravel().conj(), rcond=None)[
        0
    ].conj()


def yulewalk(
    order: int, frequencies: np.ndarray, magnitudes: np.ndarray, npt: int = 512
) -> tuple[np.ndarray, np.ndarray]:
    """
    使用改进的 Yule-Walker 方法设计逼近任意频率响应的递归（IIR）数字滤波器。
    这是 MATLAB/Octave ``yulewalk`` 的无额外依赖实现，使下方的等响度滤波器
    不再依赖第三方软件包。

    https://en.wikipedia.org/wiki/Autoregressive_model#Yule%E2%80%93Walker_equations

    :param order: 待设计滤波器的阶数
    :param frequencies: ``[0, 1]`` 上的采样点，其中 1 表示奈奎斯特频率；
        采样点从 0 开始并按递增顺序排列
    :param magnitudes: ``frequencies`` 中各点所需的线性幅值
    :param npt: 用于估计频率响应的点数
    :return: ``(a_coeffs, b_coeffs)``，即分母多项式和分子多项式

    >>> a, b = yulewalk(4, np.array([0.0, 0.5, 1.0]), np.array([1.0, 0.5, 0.0]))
    >>> len(a), len(b)
    (5, 5)
    >>> bool(np.all(np.abs(np.roots(a)) < 1))  # the designed filter is stable
    True

    输入长度不匹配或频率未按递增顺序排列时将被拒绝：

    >>> yulewalk(4, np.array([0.0, 1.0]), np.array([1.0]))
    Traceback (most recent call last):
        ...
    ValueError: frequencies and magnitudes must have the same length
    >>> yulewalk(4, np.array([0.0, 1.0, 0.5]), np.array([1.0, 0.5, 0.0]))
    Traceback (most recent call last):
        ...
    ValueError: frequencies must be in increasing order
    """
    frequencies = np.asarray(frequencies, dtype=float).ravel()
    magnitudes = np.asarray(magnitudes, dtype=float).ravel()
    if frequencies.size != magnitudes.size:
        msg = "frequencies and magnitudes must have the same length"
        raise ValueError(msg)
    if np.any(np.diff(frequencies) < 0):
        msg = "frequencies must be in increasing order"
        raise ValueError(msg)

    npt = npt + 1
    # 在密集网格上线性插值目标响应，再将其镜像，构建完整的对称幅度谱。
    response = np.interp(np.linspace(0, 1, npt), frequencies, magnitudes)
    response = np.concatenate([response, response[-2:0:-1]])

    total = response.size
    half = (total + 1) // 2
    window_len = 4 * order
    index = np.arange(window_len)

    # 根据功率谱计算自相关，并使用汉明窗进行渐缩处理。
    correlation = np.real(np.fft.ifft(response * response))
    correlation = correlation[:window_len] * (
        0.54 + 0.46 * np.cos(np.pi * index / (window_len - 1))
    )
    cepstral_window = np.concatenate([[0.5], np.ones(half - 1), np.zeros(total - half)])

    # 求解 Yule-Walker 正规方程，得到分母系数。
    rmat = toeplitz(correlation[order : window_len - 1], correlation[order:0:-1])
    rhs = -correlation[order + 1 : window_len]
    denominator = np.concatenate([[1.0], np.linalg.lstsq(rmat, rhs, rcond=None)[0]])
    denominator = _polystab(denominator)

    half_correlation = correlation.copy()
    half_correlation[0] = correlation[0] / 2
    numerator = _numerator(half_correlation, denominator, order)

    padded_num = np.zeros(total)
    padded_num[: numerator.size] = numerator
    padded_den = np.zeros(total)
    padded_den[: denominator.size] = denominator

    spectrum = 2 * np.real(np.fft.fft(padded_num) / np.fft.fft(padded_den))
    complex_log = np.log(np.abs(spectrum)) + 1j * np.angle(spectrum)
    cepstrum = np.fft.ifft(
        np.exp(np.fft.fft(cepstral_window * np.fft.ifft(complex_log)))
    )
    numerator = np.real(_numerator(cepstrum[:window_len], denominator, order))
    return denominator, numerator


class EqualLoudnessFilter:
    r"""
    一种等响度滤波器，用于补偿人耳对声音的非线性响应。该滤波器通过级联
    Yule-Walker 滤波器和巴特沃思滤波器进行校正。

    设计用于 44.1 kHz 及以上的采样率。使用更低采样率时请谨慎。

    代码基于 https://bit.ly/3eqh2HU 中的 MATLAB 实现
    （为满足 ruff 要求而缩短 URL）

    目标曲线：https://i.imgur.com/3g2VfaM.png
    Yulewalk 响应：https://i.imgur.com/J9LnJ4C.png
    巴特沃思响应和总体响应：https://i.imgur.com/3g2VfaM.png

    图像及原始 MATLAB 实现由 David Robinson 于 2001 年创作

    https://en.wikipedia.org/wiki/Equal-loudness_contour

    >>> filt = EqualLoudnessFilter()
    >>> isinstance(filt.yulewalk_filter, IIRFilter)
    True
    """

    def __init__(self, samplerate: int = 44100) -> None:
        self.yulewalk_filter = IIRFilter(10)
        self.butterworth_filter = make_highpass(150, samplerate)

        # 将数据填充到奈奎斯特频率
        curve_freqs = np.array(data["frequencies"] + [max(20000.0, samplerate / 2)])
        curve_gains = np.array(data["gains"] + [140])

        # 转换为角频率
        freqs_normalized = curve_freqs / samplerate * 2
        # 将曲线反转并归一化到 0 dB
        gains_normalized = np.power(10, (np.min(curve_gains) - curve_gains) / 20)

        # 使用上方内置的 ``yulewalk`` 实现（无第三方依赖），
        # 通过对曲线进行最小二乘拟合来计算系数。
        ya, yb = yulewalk(10, freqs_normalized, gains_normalized)
        self.yulewalk_filter.set_coefficients(ya.tolist(), yb.tolist())

    def process(self, sample: float) -> float:
        """
        使用两个滤波器处理单个采样点。

        >>> filt = EqualLoudnessFilter()
        >>> filt.process(0.0)
        0.0
        """
        tmp = self.yulewalk_filter.process(sample)
        return self.butterworth_filter.process(tmp)
