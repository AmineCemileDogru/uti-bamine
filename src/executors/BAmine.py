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
from components.BAmine.src.utils.response import build_response_b
from components.BAmine.src.models.PackageModel import PackageModel


class BAmine(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        print(self.request.data)
        self.rotation_degree = self.request.get_param("Degree")
        print("self.rotation_degree:", self.rotation_degree)
        self.keep_side = self.request.get_param("KeepSide")
        print("self.keep_side:",self.keep_side)
        self.imageOne = self.request.get_param("inputImageOne")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def blurring(self, img):
        return cv2.GaussianBlur(img, (15, 15), 0)

    def run(self):
        img = Image.get_frame(img=self.imageOne, redis_db=self.redis_db)
        img.value = self.blurring(img.value)
        self.imageOne = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        self.image_one = self.imageOne  # context.image_one için
        return build_response_b(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
