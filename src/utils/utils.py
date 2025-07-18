import os
import cv2

from tensorflow.keras.models import load_model
from sdks.novavision.src.base.logger import LoggerManager
from sdks.novavision.src.base.application import Application
from sdks.novavision.src.helper.path import get_package_storage_path

logger = LoggerManager()
application = Application()

def load_model_custom(config):
    try:
        weight_name = application.get_param(config=config, name="Weights", default="my_model.h5")
        model_path = os.path.join(get_package_storage_path(), weight_name)

        if not os.path.exists(model_path):
            logger.error(f"Model not found at {model_path}")
            return None

        model = load_model(model_path)
        logger.info(f"Model loaded from {model_path}")
        return {"model": model}
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return None
