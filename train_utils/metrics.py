import tensorflow as tf
from keras.metrics import base_metric
from keras.dtensor import utils as dtensor_utils


def sparse_top_k_categorical_matches(y_true, y_pred, k=5, none_class=None):
	"""Creates float Tensor, 1.0 for label-TopK_prediction match, 0.0 for mismatch.

	Args:
	y_true: tensor of true targets.
	y_pred: tensor of predicted targets.
	k: (Optional) Number of top elements to look at for computing accuracy.
	  Defaults to 5.

	Returns:
	Match tensor: 1.0 for label-prediction match, 0.0 for mismatch.
	"""
	reshape_matches = False
	y_true = tf.convert_to_tensor(y_true)
	y_pred = tf.convert_to_tensor(y_pred)
	y_true_rank = y_true.shape.ndims
	y_pred_rank = y_pred.shape.ndims
	y_true_org_shape = tf.shape(y_true)

	# Flatten y_pred to (batch_size, num_samples) and y_true to (num_samples,)
	if (y_true_rank is not None) and (y_pred_rank is not None):
		if y_pred_rank > 2:
			y_pred = tf.reshape(y_pred, [-1, y_pred.shape[-1]])
		if y_true_rank > 1:
			#reshape_matches = True
			y_true = tf.reshape(y_true, [-1])

	if none_class is not None:
		mask = y_true != none_class
		y_true = tf.boolean_mask(y_true, mask)
		y_pred = tf.boolean_mask(y_pred, mask)
	matches = tf.cast(
		tf.math.in_top_k(
			predictions=y_pred, targets=tf.cast(y_true, 'int32'), k=k),
		dtype='float32')

	# returned matches is expected to have same shape as y_true input
	if reshape_matches:
		return tf.reshape(matches, shape=y_true_org_shape)

	return matches


class TopKAccuracy(base_metric.MeanMetricWrapper):

	@dtensor_utils.inject_mesh
	def __init__(self, k=5, name='top_k_categorical_accuracy', none_class=None, dtype=None):
		super(TopKAccuracy, self).__init__(
			lambda yt, yp, k: sparse_top_k_categorical_matches(
				tf.math.argmax(yt, axis=-1), yp, k, none_class=none_class),
			name,
			dtype=dtype,
			k=k)
