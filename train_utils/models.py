import tensorflow as tf


class PercentageModel(tf.keras.Model):
    def compute_metrics(self, x, y, y_pred, sample_weight=None):
        metric_results = super().compute_metrics(
            x, y, y_pred, sample_weight)
        for k in metric_results:
            metric_results[k] *= 100
        return metric_results
