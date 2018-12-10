from network.base import Network
from layers.conv_ops import Conv2d, ConvT2d
from layers.pool_ops import Pool2d, UnPool2d
from utilities.misc import update

class SmallNetwork(Network):

    # actual image dimensions
    IMAGE_HEIGHT = None
    IMAGE_WIDTH = None

    # transformed input dimensions for network input
    FIT_IMAGE_HEIGHT = None
    FIT_IMAGE_WIDTH = None

    IMAGE_CHANNELS = 1

    def __init__(self, weight_init=None, act_fn="lrelu", act_leak_prob=.2, batch_norm=True, layer_params=None,
                 **kwargs):
        self.weight_init = weight_init
        self.act_fn = act_fn
        self.act_leak_prob = act_leak_prob
        self.layer_params = {"conv_1_1":{"ks":3, "dilation":1 , "output_channels":64, "keep_prob":1.0,
                                         "batch_norm": batch_norm},
                             "pool_1": {"ks":2},
                             "conv_2_1": {"ks":3, "dilation":1 , "output_channels":128, "keep_prob":1.0,
                                          "batch_norm": batch_norm},
                             "pool_2": {"ks":2},
                             "conv_3_1": {"ks":3, "dilation":1 , "output_channels":256, "keep_prob":1.0,
                                          "batch_norm": batch_norm},
                             "conv_3_2": {"ks":3, "dilation":1 , "output_channels":256, "keep_prob":1.0,
                                          "batch_norm": batch_norm},
                             "pool_3": {"ks":2},
                             "conv_4_1": {"ks":7, "dilation":1 , "output_channels":4096, "keep_prob":1.0,
                                          "batch_norm": batch_norm},
                             "conv_4_2": {"ks":1, "dilation":1 , "output_channels":4096, "keep_prob":1.0,
                                          "batch_norm": batch_norm},

                             "convt_5_1": {"ks": 1, "dilation": 1, "output_channels": 4096, "keep_prob": 1.0,
                                           "batch_norm": batch_norm},
                             "convt_5_2": {"ks": 7, "dilation": 1, "output_channels": 256, "keep_prob": 1.0,
                                           "batch_norm": batch_norm},
                             "up_6": {"ks": 2, "add_to_input": True},
                             "convt_6_1": {"ks": 3, "dilation": 1, "output_channels": 256, "keep_prob": 1.0,
                                           "batch_norm": batch_norm},
                             "convt_6_2": {"ks": 3, "dilation": 1, "output_channels": 128, "keep_prob": 1.0,
                                           "batch_norm": batch_norm},
                             "up_7": {"ks": 2, "add_to_input": True},
                             "convt_7_1": {"ks": 3, "dilation": 1, "output_channels": 64, "keep_prob": 1.0,
                                           "batch_norm": batch_norm},
                             "up_8": {"ks": 2, "add_to_input": True},
                             "convt_8_1": {"ks": 3, "dilation": 1, "output_channels": 1, "keep_prob": 1.0,
                                           "batch_norm": batch_norm}}
        if layer_params:
            update(self.layer_params.update,layer_params)

        super(SmallNetwork, self).__init__(weight_init=weight_init, **kwargs)


    def init_encoder(self, **kwargs):
        layers = []
        layers.append(Conv2d(kernel_size=self.layer_params['conv_1_1']['ks'],
                             dilation=self.layer_params['conv_1_1']['dilation'],
                             weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                             output_channels=self.layer_params['conv_1_1']['output_channels'],
                             keep_prob=self.layer_params['conv_1_1']['keep_prob'],
                             batch_norm=self.layer_params['conv_1_1']['batch_norm'], name='conv_1_1'))
        layers.append(Pool2d(kernel_size=self.layer_params['pool_1']['ks'], name='pool_1'))

        layers.append(Conv2d(kernel_size=self.layer_params['conv_2_1']['ks'],
                             dilation=self.layer_params['conv_2_1']['dilation'],
                             weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                             output_channels=self.layer_params['conv_2_1']['output_channels'],
                             keep_prob=self.layer_params['conv_2_1']['keep_prob'],
                             batch_norm=self.layer_params['conv_2_1']['batch_norm'], name='conv_2_1'))
        layers.append(Pool2d(kernel_size=self.layer_params['pool_2']['ks'], name='pool_2'))

        layers.append(Conv2d(kernel_size=self.layer_params['conv_3_1']['ks'],
                             dilation=self.layer_params['conv_3_1']['dilation'],
                             weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                             output_channels=self.layer_params['conv_3_1']['output_channels'],
                             keep_prob=self.layer_params['conv_3_1']['keep_prob'],
                             batch_norm=self.layer_params['conv_3_1']['batch_norm'], name='conv_3_1'))
        layers.append(Conv2d(kernel_size=self.layer_params['conv_3_2']['ks'],
                             dilation=self.layer_params['conv_3_2']['dilation'],
                             weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                             output_channels=self.layer_params['conv_3_2']['output_channels'],
                             keep_prob=self.layer_params['conv_3_2']['keep_prob'],
                             batch_norm=self.layer_params['conv_3_2']['batch_norm'], name='conv_3_2'))
        layers.append(Pool2d(kernel_size=self.layer_params['pool_3']['ks'], name='pool_3'))

        layers.append(Conv2d(kernel_size=self.layer_params['conv_4_1']['ks'],
                             dilation=self.layer_params['conv_4_1']['dilation'],
                             weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                             output_channels=self.layer_params['conv_4_1']['output_channels'],
                             keep_prob=self.layer_params['conv_4_1']['keep_prob'],
                             batch_norm=self.layer_params['conv_4_1']['batch_norm'], name='conv_4_1'))
        layers.append(Conv2d(kernel_size=self.layer_params['conv_4_2']['ks'],
                             dilation=self.layer_params['conv_4_2']['dilation'],
                             weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                             output_channels=self.layer_params['conv_4_2']['output_channels'],
                             keep_prob=self.layer_params['conv_4_2']['keep_prob'],
                             batch_norm=self.layer_params['conv_4_2']['batch_norm'], name='conv_4_2'))
        self.encoder = layers



    def init_decoder(self, **kwargs):
        layers = []
        layers.append(ConvT2d(kernel_size=self.layer_params['convt_5_1']['ks'],
                              dilation=self.layer_params['convt_5_1']['dilation'],
                              weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                              output_channels=self.layer_params['convt_5_1']['output_channels'],
                              keep_prob=self.layer_params['convt_5_1']['keep_prob'],
                              batch_norm=self.layer_params['convt_5_1']['batch_norm'], name='convt_5_1'))
        layers.append(ConvT2d(kernel_size=self.layer_params['convt_5_2']['ks'],
                              dilation=self.layer_params['convt_5_2']['dilation'],
                              weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                              output_channels=self.layer_params['convt_5_2']['output_channels'],
                              keep_prob=self.layer_params['convt_5_2']['keep_prob'],
                              batch_norm=self.layer_params['convt_5_2']['batch_norm'], name='convt_5_2'))

        layers.append(UnPool2d(kernel_size=self.layer_params['up_6']['ks'], name='up_6',
                               add_to_input=self.layer_params['up_6']["add_to_input"]))
        layers.append(ConvT2d(kernel_size=self.layer_params['convt_6_1']['ks'],
                              dilation=self.layer_params['convt_6_1']['dilation'],
                              weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                              output_channels=self.layer_params['convt_6_1']['output_channels'],
                              keep_prob=self.layer_params['convt_6_1']['keep_prob'],
                              batch_norm=self.layer_params['convt_6_1']['batch_norm'], name='convt_6_1'))
        layers.append(ConvT2d(kernel_size=self.layer_params['convt_6_2']['ks'],
                              dilation=self.layer_params['convt_6_2']['dilation'],
                              weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                              output_channels=self.layer_params['convt_6_2']['output_channels'],
                              keep_prob=self.layer_params['convt_6_2']['keep_prob'],
                              batch_norm=self.layer_params['convt_6_2']['batch_norm'], name='convt_6_2'))

        layers.append(UnPool2d(kernel_size=self.layer_params['up_7']['ks'], name='up_7',
                               add_to_input=self.layer_params['up_7']["add_to_input"]))
        layers.append(ConvT2d(kernel_size=self.layer_params['convt_7_1']['ks'],
                              dilation=self.layer_params['convt_7_1']['dilation'],
                              weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                              output_channels=self.layer_params['convt_7_1']['output_channels'],
                              keep_prob=self.layer_params['convt_7_1']['keep_prob'],
                              batch_norm=self.layer_params['convt_7_1']['batch_norm'], name='convt_7_1'))

        layers.append(UnPool2d(kernel_size=self.layer_params['up_8']['ks'], name='up_8',
                               add_to_input=self.layer_params['up_8']["add_to_input"]))
        layers.append(ConvT2d(kernel_size=self.layer_params['convt_8_1']['ks'],
                              dilation=self.layer_params['convt_8_1']['dilation'],
                              weight_init=self.weight_init, act_fn=None,
                              output_channels=self.layer_params['convt_8_1']['output_channels'],
                              keep_prob=self.layer_params['convt_8_1']['keep_prob'],
                              batch_norm=self.layer_params['convt_8_1']['batch_norm'], name='convt_8_1'))
        self.decoder = layers