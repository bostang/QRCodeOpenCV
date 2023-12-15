import cv2
import math

# Fungsi untuk menghitung jumlah anak dari suatu kontur dalam hirarki
def count_children(hierarchy, idx):
    count = 0
    i = hierarchy[idx][2]
    while i != -1:
        count += 1
        i = hierarchy[i][0]
    return count

# Fungsi untuk memeriksa apakah suatu kontur memiliki parent yang merupakan persegi
def has_square_parent(hierarchy, square_indices, idx):
    parent = hierarchy[idx][3]
    while parent != -1:
        if parent in square_indices:
            return True
        parent = hierarchy[parent][3]
    return False

# Konstanta toleransi persegi
# SQUARE_TOLERANCE = 0.2
BLUR_VALUE = 3
SQUARE_TOLERANCE = 10
AREA_TOLERANCE = 0.15
DISTANCE_TOLERANCE = 0.25
WARP_DIM = 300
SMALL_DIM = 29


# Load citra input
# input_image = cv2.imread('after_gaussian.jpg')
input_image = cv2.imread('after_gaussian.jpg') 

# Ubah citra input menjadi citra skala abu-abu
gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

# Deteksi tepi menggunakan metode Canny
edged = cv2.Canny(gray, 30, 200)

# Temukan kontur dan hirarki
contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Inisialisasi daftar persegi
squares = []
square_indices = []

# Iterasi melalui kontur
i = 0
for c in contours:
    # Approximate the contour
    peri = cv2.arcLength(c, True)
    area = cv2.contourArea(c)
    approx = cv2.approxPolyDP(c, 0.03 * peri, True)

    # Filter kontur yang memiliki empat sudut (quadrilateral)
    if len(approx) == 4:
        # Determine if quadrilateral is a square to within SQUARE_TOLERANCE
        if (
            area > 0
            and 1 - SQUARE_TOLERANCE < math.fabs((peri / 4) ** 2) / area < 1 + SQUARE_TOLERANCE
            and count_children(hierarchy[0], i) >= 2
            and not has_square_parent(hierarchy[0], square_indices, i)
        ):
            squares.append(approx)
            square_indices.append(i)
    i += 1

# Gambar kontur persegi pada citra asli
square_image = input_image.copy()
cv2.drawContours(square_image, squares, -1, (0, 0, 255), 2)

# Tampilkan citra input, citra hasil deteksi tepi, dan citra dengan kontur persegi
cv2.imshow('Citra Asli', input_image)
cv2.imshow('Hasil Deteksi Tepi', edged)
cv2.imshow('Citra dengan Kontur Persegi', square_image)
print(squares)
cv2.imwrite('contour_persegi.jpg', square_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
