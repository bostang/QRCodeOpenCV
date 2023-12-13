'''
Program DisplayImage
    Membuat sebuah image file dan menampilkannya
'''

# Kamus
    # Variabel
        # img : image
# Algoritma Utama

import cv2

img = cv2.imread('python.png')

cv2.imshow('sample image',img)

cv2.waitKey(0) # waits until a key is pressed
cv2.destroyAllWindows() # destroys the window showing image