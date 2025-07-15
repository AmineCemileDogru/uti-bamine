"""
    It is one of the preprocessing components in which the image is rotated.
"""

import os
import cv2
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.BAmine.src.utils.response import build_response_c
from components.BAmine.src.models.PackageModel import PackageModel


class CAmine(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.rotation_degree = self.request.get_param("Degree")
        self.keep_side = self.request.get_param("KeepSide")
        self.imageOne = self.request.get_param("inputImageOne")
        self.imageTwo = self.request.get_param("inputImageTwo")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def crop(self, img):
        return img[50:180, 100:300]

    def run(self):
        img1 = Image.get_frame(img=self.imageOne, redis_db=self.redis_db)
        img1.value = self.crop(img1.value)
        self.imageOne = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)

        img2 = Image.get_frame(img=self.imageTwo, redis_db=self.redis_db)
        img2.value = self.crop(img2.value)
        self.imageTwo = Image.set_frame(img=img2, package_uID=self.uID, redis_db=self.redis_db)

        self.image_one = self.imageOne  # context.image_one için
        self.image_two = self.imageTwo  # context.image_two için
        return build_response_c(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()