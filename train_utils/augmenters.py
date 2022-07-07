from PIL import Image
import tensorflow as tf
from tensorflow.keras.layers.experimental.preprocessing \
	import RandomFlip, RandomTranslation, RandomRotation, RandomZoom


def data_augmenter():
	data_augmentation = tf.keras.Sequential()
	data_augmentation.add(RandomFlip('horizontal'))
	data_augmentation.add(RandomZoom((-0.2, 0)))
	data_augmentation.add(RandomRotation(0.15))
	return data_augmentation


def data_augmenter_fruit360():
	data_augmentation = tf.keras.Sequential()
	data_augmentation.add(RandomFlip('horizontal'))
	data_augmentation.add(
		RandomZoom(
			(1, 1),
			fill_mode='constant',
			fill_value=255
		)
	)
	data_augmentation.add(
		RandomTranslation(
			(-0.25, 0.2),
			(-0.25, 0.2),
			fill_mode='constant',
			fill_value=255
		)
	)
	data_augmentation.add(
		RandomRotation(
			1,
			fill_mode='constant',
			fill_value=255
		)
	)
	return data_augmentation
