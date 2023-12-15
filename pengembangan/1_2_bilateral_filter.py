import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load citra input
input_image = cv2.imread('bostang_bnw.png')

# Ubah citra input menjadi citra skala abu-abu
gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

# Terapkan filter bilateral
filtered_image = cv2.bilateralFilter(gray, 11, 17, 17)

# Tampilkan citra input dan output
plt.subplot(121), plt.imshow(cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)), plt.title('Citra grayscale')
plt.subplot(122), plt.imshow(filtered_image, cmap='gray'), plt.title('Citra Setelah Filter Bilateral')
plt.show()

cv2.imwrite('after_bilateral.jpg', filtered_image)

