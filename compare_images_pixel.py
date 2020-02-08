import cv2
import numpy as np
# Truncated Images allow
# ImageFile.LOAD_TRUNCATED_IMAGES = True


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


if __name__ == '__main__':
    img1 = cv2.imread('D:/DownLoad/50k.png')
    img2 = cv2.imread('D:/DownLoad/200.png')
    # img3 = cv2.imread('D:/EVA-Space-Center-Data-Generate/src/Single_Image_negative_surface.png')
    # img4 = cv2.imread('D:/EVA-Space-Center-Data-Generate/src/Single_Image_positive_surface.png')
    err1 = mse(img1, img2)
    print(err1)
    # err2 = mse(img2, img3)
    # print(err2)
    # err3 = mse(img3, img4)
    # print(err3)
    # err4 = mse(img4, img1)
    # print(err4)
