'''
Program QRCodeDetectImage
    Mendeteksi QRCode dari sebuah input gambar
'''

# Kamus
    # Variabel
        # img1 : image
        # img2 : image
        
# Algoritma Utama
import cv2
print(cv2.__version__)
img1 = cv2.imread('./src/img/qrcodes_2.jpeg')
cv2.imshow('Input image',img1)
qcd = cv2.QRCodeDetector()
retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img1)
print(img1)
print(type(img1))
print(retval)
print(decoded_info)
print(type(points))
print(points)
print(points.shape)
print(type(straight_qrcode))
print(type(straight_qrcode[0]))
print(straight_qrcode[0].shape)

img1 = cv2.polylines(img1, points.astype(int), True, (0, 255, 0), 3)
for s, p in zip(decoded_info, points):
    img1 = cv2.putText(img1, s, p[0].astype(int),
                      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

cv2.imwrite('qrcode_opencv.jpg', img1)
# cv2.imshow('Input image',img1)
cv2.imshow('Output image',img1)

cv2.waitKey(0) # waits until a key is pressed
cv2.destroyAllWindows() # destroys the window showing image

# Referensi
    # https://note.nkmk.me/en/python-opencv-qrcode/