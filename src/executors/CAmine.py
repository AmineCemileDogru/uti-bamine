"""
    It is one of the preprocessing components in which the image is cropped.
"""

import os
import cv2
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.CAmine.src.utils.response import build_response_c
from components.CAmine.src.models.PackageModel import PackageModel


class CAmine(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.crop_type = self.request.get_param("CropType")
        self.crop_box_size = self.request.get_param("CropBoxSize", default=100)
        self.crop_ratio = self.request.get_param("CropRatio", default=0.5)
        self.imageOne = self.request.get_param("inputImageOne")
        self.imageTwo = self.request.get_param("inputImageTwo")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def crop(self, img):
        if self.crop_type == "Fixed":
            # Sabit kutu kesme (örneğin: 100x100)
            return img[50:50+self.crop_box_size, 50:50+self.crop_box_size]
        elif self.crop_type == "Ratio":
            h, w = img.shape[:2]
            new_h = int(h * self.crop_ratio)
            new_w = int(w * self.crop_ratio)
            start_y = (h - new_h) // 2
            start_x = (w - new_w) // 2
            return img[start_y:start_y+new_h, start_x:start_x+new_w]
        else:
            return img  # Geçersiz durumda orijinal döndür

    def run(self):
        img1 = Image.get_frame(img=self.imageOne, redis_db=self.redis_db)
        img1.value = self.crop(img1.value)
        self.imageOne = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)

        img2 = Image.get_frame(img=self.imageTwo, redis_db=self.redis_db)
        img2.value = self.crop(img2.value)
        self.imageTwo = Image.set_frame(img=img2, package_uID=self.uID, redis_db=self.redis_db)

        self.image_one = self.imageOne
        self.image_two = self.imageTwo
        return build_response_c(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
