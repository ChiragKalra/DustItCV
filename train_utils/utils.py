import tensorflow as tf


def is_in(a, b):
    tile_multiples = tf.concat(
        [
            tf.ones(tf.shape(tf.shape(a)), dtype=tf.int32),
            tf.shape(b)
        ],
        axis=0
    )
    a_tile = tf.tile(tf.expand_dims(a, -1), tile_multiples)
    a_tile = tf.cast(a_tile, dtype=tf.int32)
    a_in_b = tf.reduce_any(tf.equal(a_tile, b), -1)
    return a_in_b


def preprocess_bbox(before_size, after_size, bbox):
    return bbox
