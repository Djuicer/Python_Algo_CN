from PIL import Image

"""
用于图像处理的均值阈值算法。
https://en.wikipedia.org/wiki/Thresholding_(image_processing)
"""


def mean_threshold(image: Image.Image) -> Image.Image:
    """
    image：PIL 灰度图像对象
    """
    height, width = image.size
    mean = 0
    pixels = image.load()
    for i in range(width):
        for j in range(height):
            pixel = pixels[j, i]
            mean += pixel
    mean //= width * height

    for j in range(width):
        for i in range(height):
            pixels[i, j] = 255 if pixels[i, j] > mean else 0
    return image


if __name__ == "__main__":
    image = mean_threshold(Image.open("path_to_image").convert("L"))
    image.save("output_image_path")
