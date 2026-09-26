from __future__ import annotations


class IIRFilter:
    r"""
    N 阶 IIR 滤波器。
    假定处理的是归一化到 [-1, 1] 的浮点采样值。

    ---

    实现细节：
    基于以下页面中的二阶函数：
    https://en.wikipedia.org/wiki/Digital_biquad_filter,
    将其推广为 N 阶函数。

    使用以下传递函数：
        .. math:: H(z)=\frac{b_{0}+b_{1}z^{-1}+b_{2}z^{-2}+...+b_{k}z^{-k}}
                  {a_{0}+a_{1}z^{-1}+a_{2}z^{-2}+...+a_{k}z^{-k}}

    可将其改写为：
        .. math:: y[n]={\frac{1}{a_{0}}}
                  \left(\left(b_{0}x[n]+b_{1}x[n-1]+b_{2}x[n-2]+...+b_{k}x[n-k]\right)-
                  \left(a_{1}y[n-1]+a_{2}y[n-2]+...+a_{k}y[n-k]\right)\right)
    """

    def __init__(self, order: int) -> None:
        self.order = order

        # a_{0} ... a_{k}
        self.a_coeffs = [1.0] + [0.0] * order
        # b_{0} ... b_{k}
        self.b_coeffs = [1.0] + [0.0] * order

        # x[n-1] ... x[n-k]
        self.input_history = [0.0] * self.order
        # y[n-1] ... y[n-k]
        self.output_history = [0.0] * self.order

    def set_coefficients(self, a_coeffs: list[float], b_coeffs: list[float]) -> None:
        """
        设置 IIR 滤波器的系数。
        两组系数的长度都应为 `order` + 1。
        可以省略 :math:`a_0`，此时默认值为 1.0。

        此方法可与 scipy 的滤波器设计函数配合使用。

        >>> # Make a 2nd-order 1000Hz butterworth lowpass filter
        >>> import scipy.signal
        >>> b_coeffs, a_coeffs = scipy.signal.butter(2, 1000,
        ...                                          btype='lowpass',
        ...                                          fs=48000)
        >>> filt = IIRFilter(2)
        >>> filt.set_coefficients(a_coeffs, b_coeffs)

        可以省略首项系数 :math:`a_0`，其默认值为 1.0：

        >>> filt = IIRFilter(2)
        >>> filt.set_coefficients([-1.9, 0.9], [1.0, -2.0, 1.0])
        >>> filt.a_coeffs
        [1.0, -1.9, 0.9]

        传入数量错误的系数会引发 ``ValueError``：

        >>> IIRFilter(2).set_coefficients([1.0, 2.0, 3.0, 4.0], [1.0, 2.0, 3.0])
        Traceback (most recent call last):
            ...
        ValueError: Expected a_coeffs to have 3 elements for 2-order filter, got 4
        >>> IIRFilter(2).set_coefficients([1.0, 2.0, 3.0], [1.0, 2.0])
        Traceback (most recent call last):
            ...
        ValueError: Expected b_coeffs to have 3 elements for 2-order filter, got 2

        当 ``a_coeffs`` 的长度确实过短时，报告其实际长度，而不是补入可选的
        ``a_0`` 后的长度：

        >>> IIRFilter(2).set_coefficients([1.0], [1.0, 2.0, 3.0])
        Traceback (most recent call last):
            ...
        ValueError: Expected a_coeffs to have 3 elements for 2-order filter, got 1
        """
        if len(a_coeffs) == self.order:
            # 首项系数 a_0 可省略；省略时使用默认值 1.0。
            # 此方式只补入一个缺失系数，以便对长度确实过短的输入报告实际长度。
            a_coeffs = [1.0, *a_coeffs]

        if len(a_coeffs) != self.order + 1:
            msg = (
                f"Expected a_coeffs to have {self.order + 1} elements "
                f"for {self.order}-order filter, got {len(a_coeffs)}"
            )
            raise ValueError(msg)

        if len(b_coeffs) != self.order + 1:
            msg = (
                f"Expected b_coeffs to have {self.order + 1} elements "
                f"for {self.order}-order filter, got {len(b_coeffs)}"
            )
            raise ValueError(msg)

        self.a_coeffs = a_coeffs
        self.b_coeffs = b_coeffs

    def process(self, sample: float) -> float:
        """
        计算 :math:`y[n]`。

        >>> filt = IIRFilter(2)
        >>> filt.process(0)
        0.0
        """
        result = 0.0

        # 从索引 1 开始，最后处理索引 0。
        for i in range(1, self.order + 1):
            result += (
                self.b_coeffs[i] * self.input_history[i - 1]
                - self.a_coeffs[i] * self.output_history[i - 1]
            )

        result = (result + self.b_coeffs[0] * sample) / self.a_coeffs[0]

        self.input_history[1:] = self.input_history[:-1]
        self.output_history[1:] = self.output_history[:-1]

        self.input_history[0] = sample
        self.output_history[0] = result

        return result
