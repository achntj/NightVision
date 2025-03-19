import sys
from PIL import Image
import matplotlib.pyplot as plt

from basic import report

histograms = []

image_paths = sys.argv[1:]
for image_path in image_paths:
    image = Image.open(image_path)
    gray_image = image.convert('L')
    histogram = gray_image.histogram()
    histograms.append(histogram)
    report(image, image_path)

num_images = len(image_paths)
fig, axes = plt.subplots(1, num_images, figsize=(5 * num_images, 6))

if num_images == 1:
    axes = [axes]

for i, histogram in enumerate(histograms):
    axes[i].bar(range(256), histogram, width=1, color='gray')
    axes[i].set_title(image_paths[i])
    axes[i].set_xlabel('Pixel Brightness')
    axes[i].set_ylabel('Frequency')

plt.tight_layout()
plt.show()
