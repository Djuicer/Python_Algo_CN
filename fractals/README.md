# 分形

分形是一种具有*自相似性*的几何图形：放大其中一部分时，会看到整体的副本。
分形出现在数学、物理、计算机图形学乃至生物学中（例如海岸线、蕨类和雪花）。

本目录收录了一些小型、独立的分形生成器，分为两类：

- **可视化演示**：通过 `turtle` 打开窗口，或通过 `matplotlib`/`PIL` 生成图像。
  直接运行即可查看图形。
- **纯计算**生成器：其输出可用 `doctest` 检查，因此无需显示器也能在 CI 中运行。

## 内容

| 文件 | 分形 | 输出 | 说明 |
| ---- | ------- | ------ | ----- |
| [`barnsley_fern.py`](barnsley_fern.py) | 巴恩斯利蕨 | matplotlib（可选） | 迭代函数系统；设置种子后结果确定 |
| [`julia_sets.py`](julia_sets.py) | 朱利亚集 | matplotlib | 复平面逃逸时间分形 |
| [`koch_snowflake.py`](koch_snowflake.py) | 科赫雪花 | matplotlib | 线段细分 |
| [`mandelbrot.py`](mandelbrot.py) | 曼德勃罗集 | PIL 图像 | 复平面逃逸时间分形 |
| [`sierpinski_carpet.py`](sierpinski_carpet.py) | 谢尔宾斯基地毯 | 文本 | 整数运算，具有完整 doctest |
| [`sierpinski_triangle.py`](sierpinski_triangle.py) | 谢尔宾斯基三角形 | turtle | 递归中点细分 |
| [`vicsek.py`](vicsek.py) | 维切克分形 | turtle | 递归十字图案 |

## 运行

```bash
# 文本分形——输出到终端
python fractals/sierpinski_carpet.py

# 图像分形——打开 matplotlib 窗口（需要 matplotlib）
python fractals/barnsley_fern.py

# turtle 分形——打开绘图窗口（需要显示环境）
python fractals/vicsek.py
```

## 延伸阅读

- Benoit B. Mandelbrot, *The Fractal Geometry of Nature* (1982)
- Michael Barnsley, *Fractals Everywhere* (1988)
- <https://en.wikipedia.org/wiki/Fractal>
