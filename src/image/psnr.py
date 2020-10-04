from math import log10, sqrt 
import numpy as np


def image_PSNR(original, modified):
    mse = np.mean((original - modified) ** 2)
    if mse == 0:
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr
