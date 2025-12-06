# auto generated
import cv2 as cv
image = cv.imread('input_image/image_resized.png')
image = cv.rectangle(image, (48, 134), (363, 520), color=(0, 255, 0), thickness=2)
image = cv.rectangle(image, (418, 72), (872, 544), color=(0, 255, 0), thickness=2)
cv.imshow('Image with Bounding Box', image)
cv.waitKey(0)
