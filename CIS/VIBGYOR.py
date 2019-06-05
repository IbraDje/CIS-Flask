import numpy as np


def VIBGYORsegmentation(image, color):
    if len(image.shape) != 3:
        raise Exception("the image must be a 3D Numpy Array")
    if image.shape[2] != 3:
        raise Exception("plane must be equal to 3")
    C = np.zeros(shape=image.shape)
    if np.max(image) > 1:
        GL = 255
    else:
        GL = 1
    if color.upper() == 'V':
        f1, f2, f3 = (GL * 1), (GL * 0.6), (GL * 0.68)
        f4, f5, f6 = (GL * 0), (GL * 1), (GL * 0.6)
        C = cfilter(image, f1, f2, f3, f4, f5, f6, 3, 1)/GL
    elif color.upper() == 'I':
        f1, f2, f3 = (GL * 0.68), (GL * 0), (GL * 1)
        f4, f5, f6 = (GL * 0.6), (GL * 1), (GL * 0.6)
        C = cfilter(image, f1, f2, f3, f4, f5, f6, 1, 1)/GL
    elif color.upper() == 'B':
        f1, f2, f3 = (GL * 0.5), (GL * 0), (GL * 0.68)
        f4, f5, f6 = (GL * 0), (GL * 1), (GL * 0.4)
        C = cfilter(image, f1, f2, f3, f4, f5, f6, 3, 0)/GL
    elif color.upper() == 'G':
        f1, f2, f3 = (GL * 0.68), (GL * 0), (GL * 1)
        f4, f5, f6 = (GL * 0.4), (GL * 0.68), (GL * 0)
        C = cfilter(image, f1, f2, f3, f4, f5, f6, 2, 0)/GL
    elif color.upper() == 'Y':
        f1, f2, f3 = (GL * 1), (GL * 0.78), (GL * 1)
        f4, f5, f6 = (GL * 0.72), (GL * 0.52), (GL * 0)
        C = cfilter(image, f1, f2, f3, f4, f5, f6, 1, 1)/GL
    elif color.upper() == 'O':
        f1, f2, f3 = (GL * 1), (GL * 0.6), (GL * 0.68)
        f4, f5, f6 = (GL * 0.3), (GL * 0.3), (GL * 0)
        C = cfilter(image, f1, f2, f3, f4, f5, f6, 1, 0)/GL
    elif color.upper() == 'R':
        f1, f2, f3 = (GL * 1), (GL * 0.4), (GL * 0.5)
        f4, f5, f6 = (GL * 0), (GL * 0.5), (GL * 0)
        C = cfilter(image, f1, f2, f3, f4, f5, f6, 1, 0)/GL
    else:
        raise Exception("Unkown color name")
    return C


def cfilter(image, f1, f2, f3, f4, f5, f6, m, flg):
    C = np.zeros(shape=image.shape)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if flg == 0:
                if (f2 <= image[i, j, 0] <= f1
                    and f4 <= image[i, j, 1] <= f3
                    and f6 <= image[i, j, 2] <= f5
                        and image[i, j, m-1] == np.max(image[i, j])):
                    C[i, j] = image[i, j]
                else:
                    C[i, j] = image[i, j, 0] * 0.3 + image[
                        i, j, 1] * 0.59 + image[i, j, 2] * 0.11
            else:
                if (f2 <= image[i, j, 0] <= f1
                    and f4 <= image[i, j, 1] <= f3
                        and f6 <= image[i, j, 2] <= f5):
                    C[i, j] = image[i, j]
                else:
                    C[i, j] = image[i, j, 0] * 0.3 + image[
                        i, j, 1] * 0.59 + image[i, j, 2] * 0.11
    return C
