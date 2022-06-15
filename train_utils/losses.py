import tensorflow as tf
from tensorflow.math import log


def binary_crossentropy_loss(label, prediction):
	epsilon = tf.where(prediction > 0.5, tf.constant(-0.00001), tf.constant(0.00001))
	log_pred = tf.math.log(prediction + epsilon, name='Prediction_Log')
	log_pred_2 = tf.math.log(1-prediction + epsilon, name='1-Prediction_Log')
	cross_entropy = -tf.multiply(label, log_pred) - tf.multiply((1-label), log_pred_2)
	return tf.math.reduce_mean(cross_entropy)


def binary_focal_crossentropy_loss(gamma, epsilon=0.00001):
	gamma = tf.constant(gamma)
	def func(label, prediction):
		E = tf.where(prediction > 0.5, tf.constant(-epsilon), tf.constant(epsilon))
		cross_entropy = - label * log(prediction + E) * (1 - prediction) ** gamma - (1-label) * log(1-prediction + E) * prediction ** gamma
		return tf.math.reduce_mean(cross_entropy)
	return func


def categorical_crossentropy_loss(label, prediction):
	epsilon = tf.where(prediction > 0.5, tf.constant(-0.00001), tf.constant(0.00001))
	log_pred = tf.math.log(prediction + epsilon, name='Prediction_Log')
	cross_entropy = -tf.multiply(label, log_pred)
	return tf.math.reduce_mean(cross_entropy)
