# 音频滤波器

音频滤波器通过处理音频信号的频率来衰减不需要的频率并增强所需频率。
从无线电通信到高保真音响系统，任何与声音有关的领域都会使用它们。
如果你曾在立体声音响上增强低音或削弱高音、将收音机调到某个电台，
或消除录音中的背景嗡声，那么你已经使用过音频滤波器。

想进一步了解？以下资料很适合作为起点：

* <https://www.masteringbox.com/filter-types/>
* <http://ethanwiner.com/filters.html>
* <https://en.wikipedia.org/wiki/Audio_filter>
* <https://en.wikipedia.org/wiki/Electronic_filter>
* <https://webaudio.github.io/Audio-EQ-Cookbook/audio-eq-cookbook.html>

## 本目录包含的内容

| 文件 | 说明 |
| ---- | ----------- |
| [`iir_filter.py`](iir_filter.py) | 通用的 N 阶[无限脉冲响应（IIR）](https://en.wikipedia.org/wiki/Infinite_impulse_response)滤波器。它是下列所有滤波器的运行核心：为其提供一组系数，它便会逐个处理采样点流。 |
| [`butterworth_filter.py`](butterworth_filter.py) | 一组源自 RBJ Audio EQ Cookbook 的二阶[巴特沃思](https://en.wikipedia.org/wiki/Butterworth_filter)／双二阶滤波器设计。每个函数都返回一个可直接使用的 `IIRFilter`。 |
| [`equal_loudness_filter.py`](equal_loudness_filter.py) | 一种[等响度](https://en.wikipedia.org/wiki/Equal-loudness_contour)滤波器，通过级联 Yule-Walker 滤波器和巴特沃思高通滤波器，补偿人耳对声音的非线性响应。其中包含无额外依赖的 `yulewalk` 实现。 |
| [`show_response.py`](show_response.py) | 用于绘制任意滤波器[幅频响应和相频响应](https://en.wikipedia.org/wiki/Frequency_response)的辅助函数，以便直观了解滤波效果。 |
| [`loudness_curve.json`](loudness_curve.json) | 等响度滤波器所使用的 Robinson-Dadson 等响度曲线数据。 |

## `butterworth_filter.py` 中的滤波器设计

| 函数 | 效果 |
| -------- | ------ |
| `make_lowpass` | 使低于截止频率的频率通过，衰减高于截止频率的频率。 |
| `make_highpass` | 使高于截止频率的频率通过，衰减低于截止频率的频率。 |
| `make_bandpass` | 使中心频率周围的一个频带通过（裙边增益恒定）。 |
| `make_bandpass_peak` | 使中心频率周围的一个频带通过（峰值增益恒为 0 dB）。 |
| `make_notch` | 阻止中心频率周围的窄频带通过，很适合消除市电嗡声。 |
| `make_allpass` | 使所有频率通过，但改变它们之间的相位关系。 |
| `make_peak` | 按给定增益增强或削弱中心频率周围的频带（参数均衡器）。 |
| `make_lowshelf` | 增强或削弱截止频率以下的所有频率。 |
| `make_highshelf` | 增强或削弱截止频率以上的所有频率。 |

## 试用示例

```python
from audio_filters.butterworth_filter import make_lowpass
from audio_filters.show_response import show_frequency_response

# A 5 kHz low-pass filter for CD-quality audio (44.1 kHz sample rate)
filt = make_lowpass(5000, 44100)

# Process samples one at a time...
filtered = [filt.process(sample) for sample in my_audio_samples]

# ...or visualise what the filter does to the spectrum:
show_frequency_response(make_lowpass(5000, 44100), 44100)
```

每个模块都有可运行的 doctest；可以阅读这些测试，查看各滤波器具体且可直接复制使用的示例。
