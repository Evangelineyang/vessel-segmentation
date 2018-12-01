"""This is the file for the DSA network subclass"""
from network.base import Network
from layers.conv2d import Conv2d
from layers.pool_2d import Pool2d
import tensorflow as tf


class LargeNetwork(Network):

    # actual image dimensions
    IMAGE_HEIGHT = None
    IMAGE_WIDTH = None

    # transformed input dimensions for network input
    FIT_IMAGE_HEIGHT = None
    FIT_IMAGE_WIDTH = None

    IMAGE_CHANNELS = 1

    def __init__(self, weight_init=None, act_fn="lrelu", act_leak_prob=.2, layer_params=None, layers=None,
                 **kwargs):
        self.layer_params = {"conv_1_1":{"ks":3, "dilation":1 , "output_channels":64, "keep_prob":1.0,
                                         "batch_norm": True, "skip": False},
                             "pool_1": {"ks":2, "skip": True},
                             "conv_2_1": {"ks":3, "dilation":1 , "output_channels":128, "keep_prob":1.0,
                                          "batch_norm": True, "skip": False},
                             "pool_2": {"ks":2, "skip": True},
                             "conv_3_1": {"ks":3, "dilation":1 , "output_channels":256, "keep_prob":1.0,
                                          "batch_norm": True, "skip": False},
                             "conv_3_2": {"ks":3, "dilation":1 , "output_channels":256, "keep_prob":1.0,
                                          "batch_norm": True, "skip": False},
                             "pool_3": {"ks":2, "skip": True},
                             "conv_4_1": {"ks":3, "dilation":1 , "output_channels":512, "keep_prob":1.0,
                                          "batch_norm": True, "skip": False},
                             "conv_4_2": {"ks":3, "dilation":1 , "output_channels":512, "keep_prob":1.0,
                                          "batch_norm": True, "skip": False},
                             "pool_4": {"ks":2, "skip": True},
                             "conv_5_1": {"ks":3, "dilation":1 , "output_channels":512, "keep_prob":1.0,
                                          "batch_norm": True, "skip": False},
                             "conv_5_2": {"ks":3, "dilation":1 , "output_channels":512, "keep_prob":1.0,
                                          "batch_norm": True, "skip": False},
                             "pool_5": {"ks":2, "skip": True},
                             "conv_6_1": {"ks":7, "dilation":1 , "output_channels":4096, "keep_prob":1.0,
                                          "batch_norm": True, "skip": False},
                             "conv_6_2": {"ks":1, "dilation":1 , "output_channels":4096, "keep_prob":1.0,
                                          "batch_norm": True, "skip": False}
                             }

        if layer_params:
            self.layer_params.update(layer_params)

        if layers == None :

            layers = list()
            layers.append(Conv2d(kernel_size=self.layer_params['conv_1_1']['ks'],
                                 dilation=self.layer_params['conv_1_1']['dilation'], act_fn=act_fn,
                                 act_leak_prob=act_leak_prob, weight_init=weight_init,
                                 output_channels=self.layer_params['conv_1_1']['output_channels'],
                                 keep_prob=self.layer_params['conv_1_1']['keep_prob'],
                                 batch_norm=self.layer_params['conv_1_1']['batch_norm'],
                                 skip_connection=self.layer_params['conv_1_1']['skip'], name='conv_1_1'))
            layers.append(Pool2d(kernel_size=self.layer_params['pool_1']['ks'],
                                 skip_connection=self.layer_params['pool_1']['skip'], name='pool_1'))

            layers.append(Conv2d(kernel_size=self.layer_params['conv_2_1']['ks'],
                                 dilation=self.layer_params['conv_2_1']['dilation'], act_fn=act_fn,
                                 act_leak_prob=act_leak_prob, weight_init=weight_init,
                                 output_channels=self.layer_params['conv_2_1']['output_channels'],
                                 keep_prob=self.layer_params['conv_2_1']['keep_prob'],
                                 batch_norm=self.layer_params['conv_2_1']['batch_norm'],
                                 skip_connection=self.layer_params['conv_2_1']['skip'], name='conv_2_1'))
            layers.append(Pool2d(kernel_size=self.layer_params['pool_2']['ks'], name='pool_2',
                                 skip_connection=self.layer_params['pool_2']['skip']))
            layers.append(Conv2d(kernel_size=self.layer_params['conv_3_1']['ks'],
                                 dilation=self.layer_params['conv_3_1']['dilation'], act_fn=act_fn,
                                 act_leak_prob=act_leak_prob, weight_init=weight_init,
                                 output_channels=self.layer_params['conv_3_1']['output_channels'],
                                 keep_prob=self.layer_params['conv_3_1']['keep_prob'],
                                 batch_norm=self.layer_params['conv_3_1']['batch_norm'],
                                 skip_connection=self.layer_params['conv_3_1']['skip'], name='conv_3_1'))
            layers.append(Conv2d(kernel_size=self.layer_params['conv_3_2']['ks'],
                                 dilation=self.layer_params['conv_3_2']['dilation'], act_fn=act_fn,
                                 act_leak_prob=act_leak_prob,weight_init=weight_init,
                                 output_channels=self.layer_params['conv_3_2']['output_channels'],
                                 keep_prob=self.layer_params['conv_3_2']['keep_prob'],
                                 batch_norm=self.layer_params['conv_3_2']['batch_norm'],
                                 skip_connection=self.layer_params['conv_3_2']['skip'], name='conv_3_2'))
            layers.append(Pool2d(kernel_size=self.layer_params['pool_3']['ks'], name='pool_3',
                                 skip_connection=self.layer_params['pool_3']["skip"]))

            layers.append(Conv2d(kernel_size=self.layer_params['conv_4_1']['ks'],
                                 dilation=self.layer_params['conv_4_1']['dilation'], act_fn=act_fn,
                                 act_leak_prob=act_leak_prob, weight_init=weight_init,
                                 output_channels=self.layer_params['conv_4_1']['output_channels'],
                                 keep_prob=self.layer_params['conv_4_1']['keep_prob'],
                                 batch_norm=self.layer_params['conv_4_1']['batch_norm'],
                                 skip_connection=self.layer_params['conv_4_1']['skip'], name='conv_4_1'))
            layers.append(Conv2d(kernel_size=self.layer_params['conv_4_2']['ks'],
                                 dilation=self.layer_params['conv_4_2']['dilation'], act_fn=act_fn,
                                 weight_init=weight_init, act_leak_prob=act_leak_prob,
                                 output_channels=self.layer_params['conv_4_2']['output_channels'],
                                 keep_prob=self.layer_params['conv_4_2']['keep_prob'],
                                 batch_norm=self.layer_params['conv_4_2']['batch_norm'],
                                 skip_connection=self.layer_params['conv_4_2']['skip'], name='conv_4_2'))
            layers.append(Pool2d(kernel_size=self.layer_params['pool_4']['ks'], name='pool_4',
                                 skip_connection=self.layer_params['pool_4']["skip"]))

            layers.append(Conv2d(kernel_size=self.layer_params['conv_5_1']['ks'],
                                 dilation=self.layer_params['conv_5_1']['dilation'], act_fn=act_fn,
                                 weight_init=weight_init, act_leak_prob=act_leak_prob,
                                 output_channels=self.layer_params['conv_5_1']['output_channels'],
                                 keep_prob=self.layer_params['conv_5_1']['keep_prob'],
                                 batch_norm=self.layer_params['conv_5_1']['batch_norm'],
                                 skip_connection=self.layer_params['conv_5_1']['skip'], name='conv_5_1'))
            layers.append(Conv2d(kernel_size=self.layer_params['conv_5_2']['ks'],
                                 dilation=self.layer_params['conv_5_2']['dilation'], act_fn=act_fn,
                                 weight_init=weight_init, act_leak_prob=act_leak_prob,
                                 output_channels=self.layer_params['conv_5_2']['output_channels'],
                                 keep_prob=self.layer_params['conv_5_2']['keep_prob'],
                                 batch_norm=self.layer_params['conv_5_2']['batch_norm'],
                                 skip_connection=self.layer_params['conv_5_2']['skip'], name='conv_5_2'))
            layers.append(Pool2d(kernel_size=self.layer_params['pool_5']['ks'], name='pool_5',
                                 skip_connection=self.layer_params['pool_5']["skip"]))

            layers.append(Conv2d(kernel_size=self.layer_params['conv_6_1']['ks'],
                                 dilation=self.layer_params['conv_6_1']['dilation'], act_fn=act_fn,
                                 weight_init=weight_init, act_leak_prob=act_leak_prob,
                                 output_channels=self.layer_params['conv_6_1']['output_channels'],
                                 keep_prob=self.layer_params['conv_6_1']['keep_prob'],
                                 batch_norm=self.layer_params['conv_6_1']['batch_norm'],
                                 skip_connection=self.layer_params['conv_6_1']['skip'], name='conv_6_1'))
            layers.append(Conv2d(kernel_size=self.layer_params['conv_6_2']['ks'],
                                 dilation=self.layer_params['conv_6_2']['dilation'], act_fn=act_fn,
                                 weight_init=weight_init, act_leak_prob=act_leak_prob,
                                 output_channels=self.layer_params['conv_6_2']['output_channels'],
                                 keep_prob=self.layer_params['conv_6_2']['keep_prob'],
                                 batch_norm=self.layer_params['conv_6_2']['batch_norm'],
                                 skip_connection=self.layer_params['conv_6_2']['skip'], name='conv_6_2'))

        super(LargeNetwork, self).__init__(layers=layers, **kwargs)