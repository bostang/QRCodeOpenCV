import cv2 
from matplotlib import pyplot as plt

img = cv2.imread("after_gaussian.jpg") # Read image 

# Setting parameter values 
t_lower = 30 # Lower Threshold 
t_upper = 200 # Upper threshold 

# Applying the Canny Edge filter 
edge = cv2.Canny(img, t_lower, t_upper) 

# cv2.imshow('original', img) 
# cv2.imshow('edge', edge) 

plt.subplot(121), plt.imshow(img, cmap='gray'), plt.title('Citra sebelum Canny Edge filter')
plt.subplot(122), plt.imshow(edge, cmap='gray'), plt.title('Citra setelah Canny Edge filter')
plt.show()

cv2.imwrite('after_canny.jpg', edge)

cv2.waitKey(0) 
cv2.destroyAllWindows() 
