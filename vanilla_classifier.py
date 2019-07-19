from keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D, Dropout, Dense
from keras.models import Sequential
from keras.optimizers import Adam
from lesion_classifier import LesionClassifier
from base_model_param import BaseModelParam

class VanillaClassifier(LesionClassifier):
    """Skin lesion classifier based on transfer learning.

    # Arguments
        base_model_param: Instance of `BaseModelParam`.
    """

    def __init__(self, input_size=(224, 224), image_data_format='channels_last', num_classes=None, batch_size=40, rescale=None, preprocessing_func=None,
        metrics=None, image_paths_train=None, categories_train=None, image_paths_val=None, categories_val=None):

        if num_classes is None:
            raise ValueError('num_classes cannot be None')

        self._model_name = 'vanilla'

        # Define vanilla CNN
        self._model = Sequential()

        self._model.add(Conv2D(filters=32, kernel_size=3, padding='same', activation='relu', input_shape=(input_size[0], input_size[1], 3)))
        self._model.add(MaxPooling2D(pool_size=2))

        self._model.add(Conv2D(filters=64, kernel_size=3, padding='same', activation='relu'))
        self._model.add(MaxPooling2D(pool_size=2))

        self._model.add(Conv2D(filters=128, kernel_size=3, padding='same', activation='relu'))
        self._model.add(MaxPooling2D(pool_size=2))

        self._model.add(Conv2D(filters=256, kernel_size=3, padding='same', activation='relu'))
        self._model.add(MaxPooling2D(pool_size=2))

        self._model.add(Dropout(rate=0.3))
        self._model.add(GlobalAveragePooling2D())
        self._model.add(Dense(num_classes, activation='softmax'))

        self._model.compile(optimizer=Adam(lr=1e-3), loss='categorical_crossentropy', metrics=metrics)

        super().__init__(
            input_size=input_size, rescale=rescale, preprocessing_func=preprocessing_func,
            image_data_format=image_data_format, batch_size=batch_size,
            image_paths_train=image_paths_train, categories_train=categories_train,
            image_paths_val=image_paths_val, categories_val=categories_val)

    def train(self, epoch_num, class_weight=None, workers=1):
        super()._train(epoch_num, self._model_name, class_weight, workers)

    @property
    def model(self):
        return self._model

    @property
    def model_name(self):
        return self._model_name