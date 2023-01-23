from asyncore import write
from PIL import Image
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def read_pixels(im):

    data = []
    tmp = []
    pixels = im.load()
    w, h = im.size

    for y in range(h):
        for x in range(w):
            tmp.append(pixels[x, y])

        data.append(tmp)
        tmp = []
    
    return data


def write_image_from_array(im, arr):

    for i, a in enumerate(arr):
        for j, b in enumerate(a):
            im.putpixel((j, i), b)
    
    return im


def switch_r_b(coordinates, color):
    x, y = coordinates
    r, g, b = color
    return (b, g, r)


def switch_g_b(coordinates, color):
    x, y = coordinates
    r, g, b = color
    return (r, b, g)

def switch_r_g(coordinates, color):
    x, y = coordinates
    r, g, b = color
    return (g, r, b)



def apply_func(im, func):

    w, h = im.size
    pixels = im.load()

    for y in range(h):
        for x in range(w):
            pixel = pixels[x, y]

            new_pixel = func((x, y), pixel)

            im.putpixel((x, y), new_pixel)

    return im




def show_images(images, names, rows, columns, save=False, save_name="unknown.png"):
    fig = plt.figure()
    fig.canvas.set_window_title('MapBot')

    for i, (img, name) in enumerate(zip(images, names)):
        fig.add_subplot(rows, columns, i + 1)
        plt.imshow(img)
        plt.axis('off')
        plt.title(name)

    if save:
        plt.savefig(save_name)

    plt.show()




def main():

    img1 = Image.open("/images/images_costarica/costa_rica.png")

    img2 = Image.open("/images/images_costarica/costa_rica.png")
    img2 = apply_func(img2, switch_r_b)
    img2.save("/images/images_costarica/costa_rica2.png")

    img3 = Image.open("/images/images_costarica/costa_rica.png")
    img3 = apply_func(img3, switch_r_g)
    img3.save("/images/images_costarica/costa_rica3.png")

    img4 = Image.open("/images/images_costarica/costa_rica.png")
    img4 = apply_func(img4, switch_g_b)
    img4.save("/images/images_costarica/costa_rica4.png")

    images = [img1, img2, img3, img4]
    image_names = ["normal", "red-blue", "red-green", "green-blue"]
    show_images(images, image_names, 2, 2, save=True, save_name="/images/images_costarica/costa_rica_all.png")


if __name__ == "__main__":
    main()


# img_name = "costa_rica.png"

# im = Image.open("/images/images_costarica/" + img_name)

#w, h = im.size
# im = im.rotate(45)
# im.save("/images/images_costarica/costa_rica2.png")

# img_name = "costa_rica.png"
# im = Image.open("/images/images_costarica/" + img_name)

# im = apply_func(im, switch_r_b)
# im.save("/images/images_costarica/costa_rica3.png")

# plt.figure(1)
# mp_im = mpimg.imread("/images/images_costarica/costa_rica3.png")
# imgplot = plt.imshow(mp_im)

# plt.figure(2)
# mp_im2 = mpimg.imread("/images/images_costarica/costa_rica.png")
# imgplot2 = plt.imshow(mp_im2)

# plt.show()




# fig = plt.figure()

# rows, columns = 2, 2

# img1 = Image.open("/images/images_costarica/costa_rica.png")

# img2 = Image.open("/images/images_costarica/costa_rica.png")
# img2 = apply_func(img2, switch_r_b)
# img2.save("/images/images_costarica/costa_rica2.png")

# fig.add_subplot(rows, columns, 1)
# plt.imshow(img1)
# plt.axis('off')
# plt.title("First")
  
# fig.add_subplot(rows, columns, 2)
# plt.imshow(img2)
# plt.axis('off')
# plt.title("Second")

# plt.show()


# p = get_pixels(im)
# im = write_image_from_array(im, p)
# im.show()


#ps = list(im.getdata())

#im_data = np.array(w, h)


# data = np.empty((h, w), dtype=tuple)


# for y in range(h):
#     for x in range(w):
#         pixel = r, g, b = pixels[x, y]

#         new_pixel = b, g, r

#         data[y, x] = new_pixel

#         pixels[x, y] = new_pixel

#         im.putpixel((x, y), new_pixel)
    

#data.reshape(1, w*h)

# print(data)

# im = Image.fromarray(data, mode="RGB")

# im.show()
