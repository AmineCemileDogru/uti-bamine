import os
import cv2

from tensorflow.keras.models import load_model
from sdks.novavision.src.base.logger import LoggerManager
from sdks.novavision.src.base.application import Application
from sdks.novavision.src.helper.path import get_package_storage_path


def load_model_custom(config):
    model_path = "storage\my_model.h5"

    if os.path.exists(model_path):
        print(f"Model yolu bulundu: {model_path}")
        try:
            model = load_model(model_path)
            print("✅ Model başarıyla yüklendi!")
            print(model.summary())  # Model yapısını ekrana yazdırır
        except Exception as e:
            print("❌ Model yüklenirken hata oluştu:")
            print(e)
    else:
        print(f"❌ Belirtilen model yolu bulunamadı: {model_path}")

    return model
