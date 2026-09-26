from math import cos, sin, sqrt, tau

from audio_filters.iir_filter import IIRFilter

"""
使用巴特沃思（Butterworth）设计创建二阶 IIR 滤波器。

代码基于 https://webaudio.github.io/Audio-EQ-Cookbook/audio-eq-cookbook.html
也可以使用 scipy.signal.butter，它应当得到相同的结果。

https://en.wikipedia.org/wiki/Butterworth_filter

本模块统一使用以下符号（取自 RBJ Audio EQ Cookbook）：
    w0     -- 归一化角频率，``2 * pi * frequency / samplerate``
    alpha  -- 带宽参数，``sin(w0) / (2 * q_factor)``
    b0..b2 -- 双二阶滤波器的前馈（分子）系数
    a0..a2 -- 双二阶滤波器的反馈（分母）系数
a/b 系数的命名与 ``IIRFilter.set_coefficients`` 及标准双二阶传递函数一致，
因此本文件中的所有滤波器均沿用这些名称。
"""


def _validate_frequency(frequency: int, samplerate: int, q_factor: float) -> None:
    """
    验证各巴特沃思滤波器工厂函数共用的参数。

    >>> _validate_frequency(1000, 48000, 1 / sqrt(2))
    >>> _validate_frequency(0, 48000, 1 / sqrt(2))
    Traceback (most recent call last):
        ...
    ValueError: frequency must be a positive integer
    >>> _validate_frequency(24000, 48000, 1 / sqrt(2))
    Traceback (most recent call last):
        ...
    ValueError: frequency must be less than half the samplerate
    >>> _validate_frequency(1000, 0, 1 / sqrt(2))
    Traceback (most recent call last):
        ...
    ValueError: samplerate must be a positive integer
    >>> _validate_frequency(1000, 48000, 0)
    Traceback (most recent call last):
        ...
    ValueError: q_factor must be positive
    """
    if not isinstance(frequency, int) or frequency <= 0:
        raise ValueError("frequency must be a positive integer")
    if not isinstance(samplerate, int) or samplerate <= 0:
        raise ValueError("samplerate must be a positive integer")
    if frequency >= samplerate / 2:
        raise ValueError("frequency must be less than half the samplerate")
    if q_factor <= 0:
        raise ValueError("q_factor must be positive")


def make_lowpass(
    frequency: int,
    samplerate: int,
    q_factor: float = 1 / sqrt(2),
) -> IIRFilter:
    """
    创建低通滤波器。

    >>> filter = make_lowpass(1000, 48000)
    >>> filter.a_coeffs + filter.b_coeffs  # doctest: +NORMALIZE_WHITESPACE
    [1.0922959556412573, -1.9828897227476208, 0.9077040443587427, 0.004277569313094809,
     0.008555138626189618, 0.004277569313094809]
    """
    _validate_frequency(frequency, samplerate, q_factor)
    w0 = tau * frequency / samplerate
    _sin = sin(w0)
    _cos = cos(w0)
    alpha = _sin / (2 * q_factor)

    b0 = (1 - _cos) / 2
    b1 = 1 - _cos

    a0 = 1 + alpha
    a1 = -2 * _cos
    a2 = 1 - alpha

    filt = IIRFilter(2)
    filt.set_coefficients([a0, a1, a2], [b0, b1, b0])
    return filt


def make_highpass(
    frequency: int,
    samplerate: int,
    q_factor: float = 1 / sqrt(2),
) -> IIRFilter:
    """
    创建高通滤波器。

    >>> filter = make_highpass(1000, 48000)
    >>> filter.a_coeffs + filter.b_coeffs  # doctest: +NORMALIZE_WHITESPACE
    [1.0922959556412573, -1.9828897227476208, 0.9077040443587427, 0.9957224306869052,
     -1.9914448613738105, 0.9957224306869052]
    """
    _validate_frequency(frequency, samplerate, q_factor)
    w0 = tau * frequency / samplerate
    _sin = sin(w0)
    _cos = cos(w0)
    alpha = _sin / (2 * q_factor)

    b0 = (1 + _cos) / 2
    b1 = -1 - _cos

    a0 = 1 + alpha
    a1 = -2 * _cos
    a2 = 1 - alpha

    filt = IIRFilter(2)
    filt.set_coefficients([a0, a1, a2], [b0, b1, b0])
    return filt


def make_bandpass(
    frequency: int,
    samplerate: int,
    q_factor: float = 1 / sqrt(2),
) -> IIRFilter:
    """
    创建带通滤波器。

    >>> filter = make_bandpass(1000, 48000)
    >>> filter.a_coeffs + filter.b_coeffs  # doctest: +NORMALIZE_WHITESPACE
    [1.0922959556412573, -1.9828897227476208, 0.9077040443587427, 0.06526309611002579,
     0, -0.06526309611002579]
    """
    _validate_frequency(frequency, samplerate, q_factor)
    w0 = tau * frequency / samplerate
    _sin = sin(w0)
    _cos = cos(w0)
    alpha = _sin / (2 * q_factor)

    b0 = _sin / 2
    b1 = 0
    b2 = -b0

    a0 = 1 + alpha
    a1 = -2 * _cos
    a2 = 1 - alpha

    filt = IIRFilter(2)
    filt.set_coefficients([a0, a1, a2], [b0, b1, b2])
    return filt


def make_allpass(
    frequency: int,
    samplerate: int,
    q_factor: float = 1 / sqrt(2),
) -> IIRFilter:
    """
    创建全通滤波器。

    >>> filter = make_allpass(1000, 48000)
    >>> filter.a_coeffs + filter.b_coeffs  # doctest: +NORMALIZE_WHITESPACE
    [1.0922959556412573, -1.9828897227476208, 0.9077040443587427, 0.9077040443587427,
     -1.9828897227476208, 1.0922959556412573]
    """
    _validate_frequency(frequency, samplerate, q_factor)
    w0 = tau * frequency / samplerate
    _sin = sin(w0)
    _cos = cos(w0)
    alpha = _sin / (2 * q_factor)

    b0 = 1 - alpha
    b1 = -2 * _cos
    b2 = 1 + alpha

    filt = IIRFilter(2)
    filt.set_coefficients([b2, b1, b0], [b0, b1, b2])
    return filt


def make_peak(
    frequency: int,
    samplerate: int,
    gain_db: float,
    q_factor: float = 1 / sqrt(2),
) -> IIRFilter:
    """
    创建峰值滤波器。

    >>> filter = make_peak(1000, 48000, 6)
    >>> filter.a_coeffs + filter.b_coeffs  # doctest: +NORMALIZE_WHITESPACE
    [1.0653405327119334, -1.9828897227476208, 0.9346594672880666, 1.1303715025601122,
     -1.9828897227476208, 0.8696284974398878]
    """
    _validate_frequency(frequency, samplerate, q_factor)
    w0 = tau * frequency / samplerate
    _sin = sin(w0)
    _cos = cos(w0)
    alpha = _sin / (2 * q_factor)
    big_a = 10 ** (gain_db / 40)

    b0 = 1 + alpha * big_a
    b1 = -2 * _cos
    b2 = 1 - alpha * big_a
    a0 = 1 + alpha / big_a
    a1 = -2 * _cos
    a2 = 1 - alpha / big_a

    filt = IIRFilter(2)
    filt.set_coefficients([a0, a1, a2], [b0, b1, b2])
    return filt


def make_lowshelf(
    frequency: int,
    samplerate: int,
    gain_db: float,
    q_factor: float = 1 / sqrt(2),
) -> IIRFilter:
    """
    创建低架滤波器。

    >>> filter = make_lowshelf(1000, 48000, 6)
    >>> filter.a_coeffs + filter.b_coeffs  # doctest: +NORMALIZE_WHITESPACE
    [3.0409336710888786, -5.608870992220748, 2.602157875636628, 3.139954022810743,
     -5.591841778072785, 2.5201667380627257]
    """
    _validate_frequency(frequency, samplerate, q_factor)
    w0 = tau * frequency / samplerate
    _sin = sin(w0)
    _cos = cos(w0)
    alpha = _sin / (2 * q_factor)
    big_a = 10 ** (gain_db / 40)
    pmc = (big_a + 1) - (big_a - 1) * _cos
    ppmc = (big_a + 1) + (big_a - 1) * _cos
    mpc = (big_a - 1) - (big_a + 1) * _cos
    pmpc = (big_a - 1) + (big_a + 1) * _cos
    aa2 = 2 * sqrt(big_a) * alpha

    b0 = big_a * (pmc + aa2)
    b1 = 2 * big_a * mpc
    b2 = big_a * (pmc - aa2)
    a0 = ppmc + aa2
    a1 = -2 * pmpc
    a2 = ppmc - aa2

    filt = IIRFilter(2)
    filt.set_coefficients([a0, a1, a2], [b0, b1, b2])
    return filt


def make_highshelf(
    frequency: int,
    samplerate: int,
    gain_db: float,
    q_factor: float = 1 / sqrt(2),
) -> IIRFilter:
    """
    创建高架滤波器。

    >>> filter = make_highshelf(1000, 48000, 6)
    >>> filter.a_coeffs + filter.b_coeffs  # doctest: +NORMALIZE_WHITESPACE
    [2.2229172136088806, -3.9587208137297303, 1.7841414181566304, 4.295432981120543,
     -7.922740859457287, 3.6756456963725253]
    """
    _validate_frequency(frequency, samplerate, q_factor)
    w0 = tau * frequency / samplerate
    _sin = sin(w0)
    _cos = cos(w0)
    alpha = _sin / (2 * q_factor)
    big_a = 10 ** (gain_db / 40)
    pmc = (big_a + 1) - (big_a - 1) * _cos
    ppmc = (big_a + 1) + (big_a - 1) * _cos
    mpc = (big_a - 1) - (big_a + 1) * _cos
    pmpc = (big_a - 1) + (big_a + 1) * _cos
    aa2 = 2 * sqrt(big_a) * alpha

    b0 = big_a * (ppmc + aa2)
    b1 = -2 * big_a * pmpc
    b2 = big_a * (ppmc - aa2)
    a0 = pmc + aa2
    a1 = 2 * mpc
    a2 = pmc - aa2

    filt = IIRFilter(2)
    filt.set_coefficients([a0, a1, a2], [b0, b1, b2])
    return filt


def make_notch(
    frequency: int,
    samplerate: int,
    q_factor: float = 1 / sqrt(2),
) -> IIRFilter:
    """
    创建陷波（带阻）滤波器，强烈衰减 ``frequency`` 附近的窄频带，
    同时保持其余频谱不变。它是带通滤波器的互补形式，常用于消除
    50/60 Hz 市电嗡声等单一音调。

    https://en.wikipedia.org/wiki/Band-stop_filter

    >>> filter = make_notch(1000, 48000)
    >>> filter.a_coeffs + filter.b_coeffs  # doctest: +NORMALIZE_WHITESPACE
    [1.0922959556412573, -1.9828897227476208, 0.9077040443587427, 1.0,
     -1.9828897227476208, 1.0]
    """
    w0 = tau * frequency / samplerate  # 中心频率，单位为弧度/采样点
    _sin = sin(w0)
    _cos = cos(w0)
    alpha = _sin / (2 * q_factor)  # 控制阻带的窄度

    # 前馈：将一对零点精确置于陷波频率上，使该频率被完全抵消，
    # 而其余频谱得以通过。
    b0 = 1.0
    b1 = -2 * _cos
    b2 = 1.0

    # 反馈：在单位圆内侧放置匹配的极点，使陷波保持狭窄，
    # 并使周围频率的增益保持平坦。
    a0 = 1 + alpha
    a1 = -2 * _cos
    a2 = 1 - alpha

    filt = IIRFilter(2)
    filt.set_coefficients([a0, a1, a2], [b0, b1, b2])
    return filt


def make_bandpass_peak(
    frequency: int,
    samplerate: int,
    q_factor: float = 1 / sqrt(2),
) -> IIRFilter:
    """
    创建峰值增益恒为 0 dB 的带通滤波器。

    与 :func:`make_bandpass` 保持裙边（边缘）增益恒定、使峰值增益随
    ``q_factor`` 增长不同，此变体会对响应进行归一化，因此无论选择何种
    ``q_factor``，峰值始终达到 0 dB。两种形式均出自 RBJ Audio EQ Cookbook。

    https://en.wikipedia.org/wiki/Band-pass_filter

    >>> filter = make_bandpass_peak(1000, 48000)
    >>> filter.a_coeffs + filter.b_coeffs  # doctest: +NORMALIZE_WHITESPACE
    [1.0922959556412573, -1.9828897227476208, 0.9077040443587427,
     0.09229595564125725, 0, -0.09229595564125725]
    """
    w0 = tau * frequency / samplerate
    _sin = sin(w0)
    _cos = cos(w0)
    alpha = _sin / (2 * q_factor)

    b0 = alpha
    b1 = 0
    b2 = -alpha

    a0 = 1 + alpha
    a1 = -2 * _cos
    a2 = 1 - alpha

    filt = IIRFilter(2)
    filt.set_coefficients([a0, a1, a2], [b0, b1, b2])
    return filt
