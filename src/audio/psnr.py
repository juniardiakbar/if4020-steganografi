import numpy as np


def audio_PSNR(original, modified):
    size = len(original)
    MSE = np.sum(pow(original[i] - modified[i], 2) for i in range(size)) / size
    maximum = np.sum(pow(modified[i], 2) for i in range(size)) / size
    PSNR = 10 * np.log10(maximum / MSE)

    return PSNR
