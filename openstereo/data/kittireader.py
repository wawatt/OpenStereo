import os

import numpy as np
import torch
from imageio.v3 import imread

from data.base_reader import BaseReader


class KittiReader(BaseReader):
    def __init__(self, root, list_file):
        super().__init__(root, list_file)

    def item_loader(self, item):
        full_paths = [os.path.join(self.root, x) for x in item]
        left_img_path, right_img_path, disp_img_path = full_paths
        left_img = imread(left_img_path).transpose(2, 0, 1).astype(np.float32)
        right_img = imread(right_img_path).transpose(2, 0, 1).astype(np.float32)
        disp_img = imread(disp_img_path).astype(np.float32) / 256.0
        disp_img = disp_img[np.newaxis, ...]
        sample = {
            'left': torch.from_numpy(left_img),
            'right': torch.from_numpy(right_img),
            'disp': torch.from_numpy(disp_img),
            'original_size': left_img.shape[-2:],
        }
        return sample


if __name__ == '__main__':
    dataset = KittiReader(root='../../data/kitti12', list_file='../../datasets/kitti12/train.txt')
    print(dataset)
    sample = dataset[0]
    print(sample)
    print(dataset[0]['left'].shape)
