import os
from torch.utils.data import Dataset
from PIL import Image
from torchvision import transforms

class LOLDataset(Dataset):
    def __init__(self, low_light_dir, high_light_dir, transform=None):
        self.low_light_dir = low_light_dir
        self.high_light_dir = high_light_dir
        self.transform = transform
        self.low_light_images = sorted(os.listdir(low_light_dir))
        self.high_light_images = sorted(os.listdir(high_light_dir))

    def __len__(self):
        return len(self.low_light_images)

    def __getitem__(self, idx):
        low_light_img_path = os.path.join(self.low_light_dir, self.low_light_images[idx])
        high_light_img_path = os.path.join(self.high_light_dir, self.high_light_images[idx])

        low_light_img = Image.open(low_light_img_path).convert('RGB')
        high_light_img = Image.open(high_light_img_path).convert('RGB')

        if self.transform:
            low_light_img = self.transform(low_light_img)
            high_light_img = self.transform(high_light_img)

        return low_light_img, high_light_img