# Код для загрузки датасета и обучения модели на распознавание зубного камня



import shutil, os
def copytree(src = './wastedata-Mask_RCNN-multiple-classes/main/Mask_RCNN', dst = '', symlinks=False, ignore=None):
    """ Функция для перемещения каталога в корневую директорию для дальнейшей работы """
    try:
        shutil.rmtree('.ipynb_checkpoints')
    except:
        pass
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
    return None
  
copytree()
shutil.copytree('./cropped_teeth','./dataset')


import os
import sys
import json
import datetime
import numpy as np
import skimage.draw
import cv2
from mrcnn.visualize import display_instances
import matplotlib.pyplot as plt

ROOT_DIR = os.path.abspath("./wastedata-Mask_RCNN-multiple-classes/main/Mask_RCNN/")
# импортируем Mask-RCNN
sys.path.append(ROOT_DIR)
from mrcnn.config import Config
from mrcnn import model as modellib, utils

# Путь к файлу с предобученными весами
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
# Директория для сохранения логов обучения и модели
DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")


class CustomConfig(Config):
    """ Конфиг для обучаемой модели """
    NAME = "object"
    IMAGES_PER_GPU = 2
    NUM_CLASSES = 1 + 1  # камень + задний фон
    STEPS_PER_EPOCH = 100
    # не определять объекты, в которых модель уверена меньше, чем на 90%.
    DETECTION_MIN_CONFIDENCE = 0.8
    MAX_GT_INSTANCE = 5


class CustomDataset(utils.Dataset):
  """ Класс для генерации набора данных для обучения"""
    def load_custom(self, dataset_dir, subset):
        name_dict = {1: "calculus"}
        name_dict_reversed = {v: k for k, v in name_dict.items()}
        """метод для загрузки датасета. 
           dataset_dir: str, директория, в которой лежит датасет;
           subset: str (train/val) тренировочная или проверочная ли выборка.
        """
        # Добавляем классы в датасет
        for k, v in name_dict.items():
          self.add_class("object", k, v)

        # проверка тренировочный или тестовый набор данных
        assert subset in ["train", "val"]
        dataset_dir = os.path.join(dataset_dir, subset)

        annotations1 = json.load(open(os.path.join(dataset_dir, "calculus_annotator.json")))
        annotations = list(annotations1.values())[1]  # don't need the dict keys
        
        # добавляем изображение
        for a in annotations:
            # добавим полигоны
            # добавим полигоны
            polygons = []
            objects = []
            for region in annotations[a]["regions"]:
                polygons.append(region["shape_attributes"])
                objects.append(list(region["region_attributes"].keys())[0])
            #polygons = [r['shape_attributes'] for r in annotations[a]['regions'] if list(r['region_attributes'].keys())[0] in name_dict.values()]
            #objects = [list(s['region_attributes'].keys())[0] for s in annotations[a]['regions'] if list(s['region_attributes'].keys())[0] in name_dict.values()]
            num_ids = [name_dict_reversed[a] for a in objects]

            # добавим изображение
            image_path = os.path.join(dataset_dir, annotations[a]["filename"])
            image = skimage.io.imread(image_path, plugin='matplotlib')
            height, width = image.shape[:2]
            self.add_image(
                "object",
                image_id=annotations[a]['filename'],
                path=image_path,
                width=width, height=height,
                polygons=polygons,
                num_ids=num_ids
                )

    def load_mask(self, image_id):
        """метод для генерации маски изображения.
       Вовзращает:
        masks: Булевый массив размерности [высота, ширина, кол-во масок]
        class_ids: одномерный массив со значениями, к какому классу относится маска
        """
        # если изображение не отнесено к распознаваемому классу
        image_info = self.image_info[image_id]
        if image_info["source"] != "object":
            return super(self.__class__, self).load_mask(image_id)

        # Конвертирует полигоны в массив из нулей/единиц (маску) формата
        # [высота, ширина, кол-во объектов]
        info = self.image_info[image_id]
        if info["source"] != "object":
            return super(self.__class__, self).load_mask(image_id)
        num_ids = info['num_ids']
        mask = np.zeros([info["height"], info["width"], len(info["polygons"])],
                        dtype=np.uint8)
        for i, p in enumerate(info["polygons"]):
            rr, cc = skimage.draw.polygon(p['all_points_y'], p['all_points_x'])
            try: 
              mask[rr, cc, i] = 1
            except: #временная конструкция для дебага неизвестной ошибки, выпадаемой, из-за какого-то забагованного изображения
              pass
              
        num_ids = np.array(num_ids, dtype=np.int32)
        return mask, num_ids

    def image_reference(self, image_id):
        """Мед, который возвращает путь к изображению по его id"""
        info = self.image_info[image_id]
        if info["source"] == "object":
            return info["path"]
        else:
            super(self.__class__, self).image_reference(image_id)


config = CustomConfig()
model = modellib.MaskRCNN(mode="training", config=config,
                                  model_dir=DEFAULT_LOGS_DIR)

weights_path = COCO_WEIGHTS_PATH
        # Загрузим файл с весами
if not os.path.exists(weights_path):
  utils.download_trained_weights(weights_path)

model.load_weights(weights_path, by_name=True, exclude=[
            "mrcnn_class_logits", "mrcnn_bbox_fc",
            "mrcnn_bbox", "mrcnn_mask"])

model.keras_model.metrics_tensors = []


def train(model):
    """Train the model."""
    # Инициализируем и обучаем обучающий датасет
    dataset_train = CustomDataset()
    dataset_train.load_custom("./dataset", "train")
    dataset_train.prepare()

    # Инициализируем валидационный датасет
    dataset_val = CustomDataset()
    dataset_val.load_custom("./dataset", "val")
    dataset_val.prepare()

    print("Training network heads")
    model.train(dataset_train, dataset_val,
                learning_rate=config.LEARNING_RATE,
                epochs=25,
                layers='heads')


train(model)