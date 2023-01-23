import cv2 
import pytesseract

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

img = cv2.imread('images/coordinates.png')
img = cv2.imread('hello_sign.jpg')
#img = get_grayscale(img)

s = pytesseract.image_to_string(img)


print(s)