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
    # prevent taking the log of zero by selecting the lowest intensity nonzero pixel
    if sample == 0:
        sample = pixels[pixels.nonzero()][0]

    exp = math.log(t) / math.log(sample)
    img = np.pow(img, exp)
    img = np.astype(img * 255, 'uint8')
    return Image.fromarray(img)


def concat_images(*imgs):
    x = sum(img.size[0] for img in imgs)
    new = Image.new('RGB', (x, imgs[0].size[1]))
    offset = 0
    for img in imgs:
        new.paste(img, (offset, 0))
        offset += img.size[0]
    return new


def report(img, name):
    print(f'Image: {name}')
    print(f'  min: {np.min(img)}')
    print(f'  max: {np.max(img)}')
    print(f'  avg: {np.mean(img)}')
    print(f'  std: {np.std(img)}')


if __name__ == '__main__':
    import sys
    import os
    def outpath(original, mod):
        path = original
        path = os.path.basename(path)
        basename = os.path.splitext(path)[0]
        return f'output/{basename}_{mod}.png'
    assert len(sys.argv) > 1
    for path in sys.argv[1:]:
        img = Image.open(path)
        report(img, f'{path} (original)')
        p = 0.5
        t = 0.37 # target an average brightness around 95
        normalized = normalize_average(img, p, t)
        report(normalized, f'{path} normalized ({p=}, {t=})')
        # concat_images(img, normalized).save(outpath(path, 'test'))
        normalized.save(outpath(path, 'bright'))

