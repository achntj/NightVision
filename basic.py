from PIL import Image, ImageFilter
import numpy as np
import math


# Linearly map the RGB values to [0-255]
# adjusts black and white point
def normalize(img):
    img = img - np.min(img)
    img = img / np.max(img)
    img = np.astype(img * 255, 'uint8')
    return Image.fromarray(img)


# adjusts black and white point then attempts to automatically gamma correct
def normalize_average(img, p, t=None):
    if t is None: t = p
    img = img - np.min(img)
    img = img / np.max(img)
    # obviously sorting every pixel of the image is not the most efficient.
    # a quickselect algorithm would be better but I don't think that's built into numpy
    pixels = img.flatten()
    pixels = np.sort(pixels)
    sample = pixels[int(p * np.size(pixels))]

    exp = math.log(t) / math.log(sample)
    img = np.pow(img, exp)
    img = np.astype(img * 255, 'uint8')
    return Image.fromarray(img)


def report(img, name):
    print(f'Image: {name}')
    print(f'  min: {np.min(img)}')
    print(f'  max: {np.max(img)}')
    print(f'  avg: {np.mean(img)}')


if __name__ == '__main__':
    import sys
    import os
    def outpath(original, mod):
        path = original
        path = os.path.basename(path)
        basename = os.path.splitext(path)[0]
        return f'output/{basename}_{mod}.png'
    path = sys.argv[1]
    img = Image.open(path)
    report(img, 'original')
    p = 0.5
    t = 0.25
    mean_norm = normalize_average(img, p, t)
    report(mean_norm, f'normalized average ({p=}, {t=})')
    mean_norm.save(outpath(path, 'bright'))

