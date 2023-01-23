import cv2 as cv
import numpy as np
# from matplotlib import pyplot as plt

def find_image(larger, smaller):

    img = cv.imread(larger, 0)
    img2 = img.copy()
    template = cv.imread(smaller, 0)
    w, h = template.shape[::-1]
    #w2, h2 = img.shape[::-1]

    # All the 6 methods for comparison in a list

    methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

    meth = methods[5]

    img = img2.copy()
    method = eval(meth)
    # Apply template Matching
    res = cv.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc

    bottom_right = (top_left[0] + w, top_left[1] + h)

    center_x = top_left[0] + (bottom_right[0] - top_left[0]) // 2
    center_y = top_left[1] + (bottom_right[1] - top_left[1]) // 2

    # cv.rectangle(img,top_left, bottom_right, 255, 2)
    # plt.subplot(121),plt.imshow(res,cmap = 'gray')
    # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),plt.imshow(img,cmap = 'gray')
    # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    # plt.suptitle(meth)
    # plt.show()

    return center_x, center_y


# https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html


# a = find_image("start.png", "multiplayer_button.png")
# print(a)