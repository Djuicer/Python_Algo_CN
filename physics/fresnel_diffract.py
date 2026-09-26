"""
标题：相干单色波场的菲涅耳衍射

菲涅耳衍射描述在小角近似下，波场在自由空间中传播或与物体相互作用时的
行为，尤其适用于近场衍射。

以下算法改编自参考资料中基于“传递函数”的方法。满足下式时为临界采样：
pixel_size = wavelength * prop_dist / side_length

等价地：
pixel_size = sqrt(wavelength * prop_dist / pixel_num)

左侧小于或大于右侧时，分别会发生欠采样或过采样。

本代码改编自：
Computational Fourier Optics: A MATLAB Tutorial by David Voelz
"""

from math import pi

import numpy as np
from scipy.fft import fft, fft2, fftshift, ifft, ifft2, ifftshift


def fresnel_diffract(
    wavefunc_0: np.ndarray, pixel_size: float, wavelength: float, prop_dist: float
) -> np.ndarray:
    """
    一维或二维波场的菲涅耳衍射。

    计算给定波场的菲涅耳衍射，适用于近场衍射。假定波场相干且为单色波。

    参数：
        wavefunc0 (np.ndarray): 未传播平面上的初始波场。
        pixel_size (float): 未传播平面上一个像素（或数据点）的物理尺寸。
        wavelength (float): 波场的波长。
        prop_dist (float): 期望的传播距离。

    异常：
        ValueError: 输入波场不是一维或二维时抛出。

    返回：
        np.ndarray: 传播平面上的波场。

    示例：
        >>> import numpy as np
        >>> res = fresnel_diffract(np.ones(64), 1, 1, 1)
        >>> res.shape
        (64,)
        >>> import numpy as np
        >>> res = fresnel_diffract(np.ones((64, 64)), 1, 1, 1)
        >>> res.shape
        (64, 64)
        >>> import numpy as np
        >>> res = fresnel_diffract(np.ones((4, 4, 4)), 1, 1, 1)
        Traceback (most recent call last):
            ...
        ValueError: Expected a 1D or 2D wavefield, but got (4, 4, 4)

        # Test that conservation of energy is obeyed
        >>> import numpy as np
        >>> wf0 = np.ones(64)
        >>> wfz = fresnel_diffract(wf0, 1, 1, 1)
        >>> bool(np.isclose(np.sum(abs(wf0)**2), np.sum(abs(wfz)**2)))
        True
        >>> import numpy as np
        >>> wf0 = np.ones((64, 64))
        >>> wfz = fresnel_diffract(wf0, 1, 1, 1)
        >>> bool(np.isclose(np.sum(abs(wf0)**2), np.sum(abs(wfz)**2)))
        True

        # Test that propagation distance of 0 returns the contact image
        >>> import numpy as np
        >>> x = np.linspace(-32, 32, 1)
        >>> wf0 = np.where(abs(x)<=8, 1, 0)
        >>> wfz = fresnel_diffract(wf0, 1, 1, 0)
        >>> np.allclose(wf0, wfz)
        True
    """

    if len(wavefunc_0.shape) == 1:
        return _fresnel_diffract_1d(wavefunc_0, pixel_size, wavelength, prop_dist)
    elif len(wavefunc_0.shape) == 2:
        return _fresnel_diffract_2d(wavefunc_0, pixel_size, wavelength, prop_dist)
    else:
        error_message = f"Expected a 1D or 2D wavefield, but got {wavefunc_0.shape}"
        raise ValueError(error_message)


def _fresnel_diffract_2d(
    wavefunc_0: np.ndarray, pixel_size: float, wavelength: float, prop_dist: float
) -> np.ndarray:
    """
    二维波场的菲涅耳衍射。
    此私有函数由 'fresnel_diffract' 调用，专门处理二维波场的菲涅耳衍射。
    参数：
        wavefunc_0 (np.ndarray): 未传播平面上的初始二维波场。
        pixel_size (float): 未传播平面上一个像素（或数据点）的物理尺寸。
        wavelength (float): 波场的波长。
        prop_dist (float): 期望的传播距离。

    返回：
        np.ndarray: 传播平面上的二维波场。


    示例：
        >>> import numpy as np
        >>> res = _fresnel_diffract_2d(np.ones((64, 64)), 1, 1, 1)
        >>> res.shape
        (64, 64)
        >>> import numpy as np
        >>> wf0 = np.ones((64, 64))
        >>> wfz = _fresnel_diffract_2d(wf0, 1, 1, 1)
        >>> bool(np.isclose(np.sum(abs(wf0)**2), np.sum(abs(wfz)**2)))
        True

        # Test that propagation distance of 0 returns the contact image
        >>> import numpy as np
        >>> x = np.linspace(-32, 32, 1)
        >>> X1, X2 = np.meshgrid(x, x)
        >>> wf0 = np.where(abs(X1)<=8, 1, 0) * np.where(abs(X2)<=8, 1, 0)
        >>> wfz = _fresnel_diffract_2d(wf0, 1, 1, 0)
        >>> np.allclose(wf0, wfz)
        True
    """
    pixel_num, _ = wavefunc_0.shape
    side_length = pixel_num * pixel_size

    # Fourier 空间中的坐标与 1 / pixel_size 成正比
    f_x = np.arange(-1 / (2 * pixel_size), 1 / (2 * pixel_size), 1 / side_length)

    f_x2d, f_y2d = np.meshgrid(f_x, f_x)

    # 模拟衍射的传递函数
    transferf = np.exp(-1j * np.pi * wavelength * prop_dist * (f_x2d**2 + f_y2d**2))
    transferf = fftshift(transferf)

    # 未传播平面上的 Fourier 空间波函数
    f_wavefunc_0 = fft2(fftshift(wavefunc_0))
    # 传播平面（即 'z' 平面）上的波函数
    wavefuncz = ifftshift(ifft2(transferf * f_wavefunc_0))

    return wavefuncz


def _fresnel_diffract_1d(
    wavefunc_0: np.ndarray, pixel_size: float, wavelength: float, prop_dist: float
) -> np.ndarray:
    """
    一维波场的菲涅耳衍射。
    此私有函数由 'fresnel_diffract' 调用，专门处理一维波场的菲涅耳衍射。
    参数：
        wavefunc0 (np.ndarray): 未传播平面上的初始一维波场。
        pixel_size (float): 未传播平面上一个像素（或数据点）的物理尺寸。
        wavelength (float): 波场的波长。
        prop_dist (float): 期望的传播距离。

    返回：
        np.ndarray: 传播平面上的一维波场。


    示例：
        >>> import numpy as np
        >>> res = _fresnel_diffract_1d(np.ones(64), 1, 1, 1)
        >>> res.shape
        (64,)

        # Conservation of energy
        >>> import numpy as np
        >>> wf0 = np.ones(64)
        >>> wfz = _fresnel_diffract_1d(wf0, 1, 1, 1)
        >>> bool(np.isclose(np.sum(abs(wf0)**2), np.sum(abs(wfz)**2)))
        True

        # Test that propagation distance of 0 returns the contact image
        >>> import numpy as np
        >>> x = np.linspace(-32, 32, 1)
        >>> wf0 = np.where(abs(x)<=8, 1, 0)
        >>> wfz = _fresnel_diffract_1d(wf0, 1, 1, 0)
        >>> np.allclose(wf0, wfz)
        True
    """
    pixel_num = len(wavefunc_0)
    side_length = pixel_num * pixel_size
    fx = np.arange(-1 / (2 * pixel_size), 1 / (2 * pixel_size), 1 / side_length)
    transferf = np.exp(-1j * pi * wavelength * prop_dist * (fx**2))
    transferf = fftshift(transferf)

    f_wavefunc_0 = fft(fftshift(wavefunc_0))

    wavefunc_z = ifftshift(ifft(transferf * f_wavefunc_0))

    return wavefunc_z
