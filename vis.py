import sys
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

from basic import report

histograms = []

image_paths = sys.argv[1:]
for image_path in image_paths:
    image = Image.open(image_path)
    gray_image = image.convert('L')
    histogram = [np.percentile(gray_image, i) for i in range(101)]
    histograms.append(histogram)
    report(image, image_path)

num_images = len(image_paths)
fig, axes = plt.subplots(1, num_images, figsize=(5 * num_images, 6))

if num_images == 1:
    axes = [axes]

for i, histogram in enumerate(histograms):
    axes[i].plot(histogram)
    axes[i].set_title(image_paths[i])
    axes[i].set_xlabel('Percentile')
    axes[i].set_ylabel('Pixel Brightness')

plt.tight_layout()
plt.show()
