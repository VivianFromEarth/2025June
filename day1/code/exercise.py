# # version1: 全通道联合归一化

import rasterio
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # 避免 macOS PyCharm 后端冲突
import matplotlib.pyplot as plt
import cv2
import os

def draw(image, title='Image'):
    plt.figure(figsize=(12, 10))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # BGR → RGB for display
    plt.title(title)
    plt.axis('off')
    plt.show()

def adjust_brightness(image, target_brightness=100):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    current_brightness = np.mean(gray)
    brightness_factor = target_brightness / current_brightness
    adjusted_image = cv2.convertScaleAbs(image, alpha=brightness_factor, beta=0)
    return adjusted_image

def shuchu(tif_file):
    with rasterio.open(tif_file) as src:
        bands = src.read()

    # 假设通道顺序为 B02, B03, B04 (Blue, Green, Red)
    blue = bands[0].astype(float)
    green = bands[1].astype(float)
    red = bands[2].astype(float)

    # ✅ 联合归一化：根据RGB三个通道的整体最小值和最大值
    stacked = np.stack([red, green, blue], axis=0)
    global_min = stacked.min()
    global_max = stacked.max()

    # 逐通道归一化到 0~255
    red_norm = ((red - global_min) / (global_max - global_min)) * 255
    green_norm = ((green - global_min) / (global_max - global_min)) * 255
    blue_norm = ((blue - global_min) / (global_max - global_min)) * 255

    # 合并为 BGR 图像（OpenCV 默认格式）
    bgr_image = cv2.merge([
        blue_norm.astype(np.uint8),
        green_norm.astype(np.uint8),
        red_norm.astype(np.uint8)
    ])

    # 可选：调整亮度
    bgr_bright = adjust_brightness(bgr_image, target_brightness=120)

    # 显示图像
    draw(bgr_bright, title='Brightness Adjusted RGB Image')

    # （可选保存）
    # output_path = os.path.join(os.path.dirname(tif_file), "output_rgb.png")
    # cv2.imwrite(output_path, bgr_bright)
    # print(f"图像已保存为：{output_path}")

# ===================== 调用主程序 =====================
if __name__ == "__main__":
    tif_path = r"/Users/weirdprincess/Downloads/2019_1101_nofire_B2348_B12_10m_roi.tif"
    shuchu(tif_path)

#version2：每通道独立归一化
# import rasterio
# import numpy as np
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
# import cv2
# import os
#
# def draw(image, title='Image'):
#     plt.figure(figsize=(12, 10))
#     plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#     plt.title(title)
#     plt.axis('off')
#     plt.show()
#
# def adjust_brightness(image, target_brightness=100):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     current_brightness = np.mean(gray)
#     brightness_factor = target_brightness / current_brightness
#     adjusted_image = cv2.convertScaleAbs(image, alpha=brightness_factor, beta=0)
#     return adjusted_image
#
# def shuchu(tif_file):
#     with rasterio.open(tif_file) as src:
#         bands = src.read()
#
#     # 波段顺序假设为 B02, B03, B04
#     blue = bands[0].astype(float)
#     green = bands[1].astype(float)
#     red = bands[2].astype(float)
#
#     # ✅ 每个通道分别归一化到 0~255
#     red_min, red_max = red.min(), red.max()
#     green_min, green_max = green.min(), green.max()
#     blue_min, blue_max = blue.min(), blue.max()
#
#     red_norm = ((red - red_min) / (red_max - red_min)) * 255
#     green_norm = ((green - green_min) / (green_max - green_min)) * 255
#     blue_norm = ((blue - blue_min) / (blue_max - blue_min)) * 255
#
#     # 合成 BGR 图像
#     bgr_image = cv2.merge([
#         blue_norm.astype(np.uint8),
#         green_norm.astype(np.uint8),
#         red_norm.astype(np.uint8)
#     ])
#
#     # 调整亮度（可选）
#     bgr_bright = adjust_brightness(bgr_image, target_brightness=120)
#
#     # 显示图像
#     draw(bgr_bright, title='Per-Channel Normalized Image')
#
# # =====================
# if __name__ == "__main__":
#     tif_path = r"/Users/weirdprincess/Downloads/2019_1101_nofire_B2348_B12_10m_roi.tif"
#     shuchu(tif_path)
#
