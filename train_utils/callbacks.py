import tensorflow as tf
import numpy as np
import keras.backend as K


class LossHistory(tf.keras.callbacks.Callback):
    def __init__(self, batches, l_r=(-5, -1)):
        super().__init__()
        self.losses = []
        self.batches = batches
        l, r = l_r
        self.exp_lrs = np.arange(l, r, step=(r - l) / self.batches)

    def on_batch_begin(self, batch, logs={}):
        lr = np.power(10, self.exp_lrs[batch])
        K.set_value(self.model.optimizer.lr, lr)

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs['loss'])


class LRCallBack(tf.keras.callbacks.Callback):
    def __init__(self, epochs, batches, l_r, start_epoch=0):
        super().__init__()
        l, r = l_r
        self.batch_losses = np.zeros(epochs * batches)
        self.batches = batches
        self.epochs = epochs
        self.start_epoch = start_epoch
        self.epoch = -1
        self.exp_lrs = np.linspace(l, r, epochs, endpoint=True)

    def on_epoch_begin(self, epoch, logs={}):
        self.epoch += 1
        lr = np.power(10, self.exp_lrs[epoch-self.start_epoch])
        K.set_value(self.model.optimizer.lr, lr)
        print('LR set to: %.6f' % lr)

    def on_batch_end(self, batch, logs={}):
        self.batch_losses[batch + self.batches*self.epoch] = logs['loss'] 
