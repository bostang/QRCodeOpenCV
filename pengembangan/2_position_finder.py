import cv2
import numpy as np

# Load citra input
# input_image = cv2.imread('after_gaussian.jpg')
input_image = cv2.imread('after_gaussian.jpg')

# Ubah citra input menjadi citra skala abu-abu
gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

# Deteksi tepi menggunakan metode Canny
edged = cv2.Canny(gray, 30, 200)

# Temukan kontur dan hirarki
contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Gambar kontur pada citra asli
contour_image = input_image.copy()
# contour_image = np.zeros_like(edged)

# cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

# Tampilkan citra input, citra hasil deteksi tepi, dan citra dengan kontur
cv2.imshow('Citra Asli', input_image)
cv2.imshow('Hasil Deteksi Tepi', edged)
cv2.imshow('Citra dengan Kontur', contour_image)
# print(contours)
# print(hierarchy)
# cv2.imwrite('contour.jpg', contour_image)


cv2.waitKey(0)
cv2.destroyAllWindows()
