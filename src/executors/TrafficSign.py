import os
import sys
import numpy as np
import cv2
from PIL import Image as PILImage

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.BAmine.src.utils.response import build_response_traffic
from components.BAmine.src.models.PackageModel import PackageModel
from components.BAmine.src.utils.utils import load_model_custom


# Sınıf label'larını burada sabitliyoruz (isteğe bağlı)
classes = {
    0: 'Speed limit (20km/h)', 1: 'Speed limit (30km/h)', 2: 'Speed limit (50km/h)',
    3: 'Speed limit (60km/h)', 4: 'Speed limit (70km/h)', 5: 'Speed limit (80km/h)',
    6: 'End of speed limit (80km/h)', 7: 'Speed limit (100km/h)', 8: 'Speed limit (120km/h)',
    9: 'No passing', 10: 'No passing for vehicles > 3.5 tons', 11: 'Right-of-way at the next intersection',
    12: 'Priority road', 13: 'Yield', 14: 'Stop', 15: 'No vehicles', 16: 'Vehicles > 3.5 tons prohibited',
    17: 'No entry', 18: 'General caution', 19: 'Dangerous curve to the left', 20: 'Dangerous curve to the right',
    21: 'Double curve', 22: 'Bumpy road', 23: 'Slippery road', 24: 'Road narrows on the right',
    25: 'Road work', 26: 'Traffic signals', 27: 'Pedestrians', 28: 'Children crossing',
    29: 'Bicycles crossing', 30: 'Beware of ice/snow', 31: 'Wild animals crossing',
    32: 'End speed + passing limits', 33: 'Turn right ahead', 34: 'Turn left ahead',
    35: 'Ahead only', 36: 'Go straight or right', 37: 'Go straight or left',
    38: 'Keep right', 39: 'Keep left', 40: 'Roundabout mandatory',
    41: 'End of no passing', 42: 'End no passing vehicles > 3.5 tons'
}


class TrafficSign(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.image = self.request.get_param("inputImageOne")
        self.model = bootstrap["model"]  # Keras model

    @staticmethod
    def bootstrap(config: dict) -> dict:
        model=load_model_custom(config=config)
        return {"model":model}

    def classify_sign(self, image_array, img_uid):
        resized = cv2.resize(image_array, (30, 30))
        normalized = resized / 255.0
        input_tensor = np.expand_dims(normalized, axis=0)

        prediction = self.model.predict(input_tensor)
        class_id = np.argmax(prediction)
        confidence = float(np.max(prediction))

        label = classes.get(class_id, str(class_id))

        # İsteğe bağlı: dummy BoundingBox (sabit kare olarak)
        from sdks.novavision.src.base.model import BoundingBox
        bbox = BoundingBox(left=0, top=0, width=30, height=30)

        return Detection(
            boundingBox=bbox,
            confidence=confidence,
            classLabel=label,
            classId=class_id,
            imgUID=img_uid
        )

    def run(self):
        img = Image.get_frame(img=self.imageOne, redis_db=self.redis_db)
        self.imageOne = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        self.image_one = self.imageOne
        packageModel = build_response_traffic(context=self)
        return packageModel


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
