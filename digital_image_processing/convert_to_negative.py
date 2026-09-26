"""
使用 OpenCV 实现将彩色图像转换为负片的算法。
"""

from cv2 import destroyAllWindows, imread, imshow, waitKey


def convert_to_negative(img):
    # 获取图像中的像素数量
    pixel_h, pixel_v = img.shape[0], img.shape[1]

    # 将每个像素的颜色转换为其负片值
    for i in range(pixel_h):
        for j in range(pixel_v):
            img[i][j] = [255, 255, 255] - img[i][j]

    return img


if __name__ == "__main__":
    # 读取原始图像
    img = imread("image_data/lena.jpg", 1)

    # 转换为负片
    neg = convert_to_negative(img)

    # 显示结果图像
    imshow("negative of original image", img)
    waitKey(0)
    destroyAllWindows()
