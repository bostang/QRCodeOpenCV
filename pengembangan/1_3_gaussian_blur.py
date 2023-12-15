import cv2
# import numpy
from matplotlib import pyplot as plt

  
# read image
src = cv2.imread('after_bilateral.jpg', cv2.IMREAD_UNCHANGED)
 
BLUR_VALUE = 3

# apply guassian blur on src image
# dst = cv2.GaussianBlur(src,(5,5),cv2.BORDER_DEFAULT)
dst = cv2.GaussianBlur(src, (BLUR_VALUE, BLUR_VALUE), 0)

# display input and output image
# cv2.imshow("Gaussian Smoothing",numpy.hstack((src, dst)))

plt.subplot(121), plt.imshow(src, cmap='gray'), plt.title('Citra sebelum Gaussian blur')
plt.subplot(122), plt.imshow(dst, cmap='gray'), plt.title('Citra setelah Gaussian blur')
plt.show()

cv2.imwrite('after_gaussian.jpg', dst)

cv2.waitKey(0) # waits until a key is pressed
cv2.destroyAllWindows() # destroys the window showing image