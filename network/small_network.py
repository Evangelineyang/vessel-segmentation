from network.base import Network
from layers.conv_ops import Conv2d, ConvT2d
from layers.pool_ops import Pool2d, UnPool2d
from utilities.misc import update
from tensorflow.keras.applications import DenseNet121, DenseNet169, DenseNet201, InceptionResNetV2, InceptionV3, \
    MobileNet, MobileNetV2, ResNet50, VGG16, VGG19, Xception, NASNetLarge
import tensorflow as tf

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
        self.layer_params = {"conv_1_1":{"kernel_size":3, "dilation":1 , "output_channels":64, "batch_norm": batch_norm,
                                         "name": "conv_1_1"},
                             "pool_1": {"kernel_size":2, "name": "pool_1"},
                             "conv_2_1": {"kernel_size":3, "dilation":1 , "output_channels":128,
                                          "batch_norm": batch_norm, "name": "conv_2_1"},
                             "pool_2": {"kernel_size":2, "name": "pool_2"},
                             "conv_3_1": {"kernel_size":3, "dilation":1 , "output_channels":256,
                                          "batch_norm": batch_norm, "name": "conv_3_1"},
                             "conv_3_2": {"kernel_size":3, "dilation":1 , "output_channels":256,
                                          "batch_norm": batch_norm, "name": "conv_3_2"},
                             "pool_3": {"kernel_size":2, "name": "pool_3"},
                             "conv_4_1": {"kernel_size":7, "dilation":1 , "output_channels":4096,
                                          "batch_norm": batch_norm, "name": "conv_4_1"},
                             "conv_4_2": {"kernel_size":1, "dilation":1 , "output_channels":4096,
                                          "batch_norm": batch_norm, "name": "conv_4_2"},
                             "convt_5_1": {"kernel_size": 1, "dilation": 1, "output_channels": 4096,
                                           "batch_norm": batch_norm, "name": "convt_5_1"},
                             "convt_5_2": {"kernel_size": 7, "dilation": 1, "output_channels": 256,
                                           "batch_norm": batch_norm, "name": "convt_5_2"},
                             "up_6": {"kernel_size": 2, "add_to_input": True, "name": "up_6"},
                             "convt_6_1": {"kernel_size": 3, "dilation": 1, "output_channels": 256,
                                           "batch_norm": batch_norm, "name": "convt_6_1"},
                             "convt_6_2": {"kernel_size": 3, "dilation": 1, "output_channels": 128,
                                           "batch_norm": batch_norm, "name": "convt_6_2"},
                             "up_7": {"kernel_size": 2, "add_to_input": True, "name": "up_7"},
                             "convt_7_1": {"kernel_size": 3, "dilation": 1, "output_channels": 64,
                                           "batch_norm": batch_norm, "name": "convt_7_1"},
                             "up_8": {"kernel_size": 2, "add_to_input": True, "name": "up_8"},
                             "convt_8_1": {"kernel_size": 3, "dilation": 1, "output_channels": 1,
                                           "batch_norm": batch_norm, "name": "convt_8_1", "act_fn": None}}
        if layer_params:
            self.layer_params = update(self.layer_params, layer_params)

        super(SmallNetwork, self).__init__(weight_init=weight_init, **kwargs)


    def init_encoder(self, **kwargs):
        layers = []
        layers.append(Conv2d(weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                             **self.layer_params["conv_1_1"]))
        layers.append(Pool2d(**self.layer_params['pool_1']))

        layers.append(Conv2d(weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                             **self.layer_params['conv_2_1']))
        layers.append(Pool2d(**self.layer_params['pool_2']))

        layers.append(Conv2d(weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                             **self.layer_params['conv_3_1']))
        layers.append(Conv2d(weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                             **self.layer_params['conv_3_2']))
        layers.append(Pool2d(**self.layer_params['pool_3']))

        layers.append(Conv2d(weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                             **self.layer_params['conv_4_1']))
        layers.append(Conv2d(weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                             **self.layer_params['conv_4_2']))
        self.encoder = layers



    def init_decoder(self, **kwargs):
        layers = []
        layers.append(ConvT2d(weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                              **self.layer_params['convt_5_1']))
        layers.append(ConvT2d(weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                              **self.layer_params['convt_5_2']))

        layers.append(UnPool2d(**self.layer_params['up_6']))
        layers.append(ConvT2d(weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                              **self.layer_params['convt_6_1']))
        layers.append(ConvT2d(weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                              **self.layer_params['convt_6_2']))

        layers.append(UnPool2d(**self.layer_params['up_7']))
        layers.append(ConvT2d(weight_init=self.weight_init, act_fn=self.act_fn, act_leak_prob=self.act_leak_prob,
                              **self.layer_params['convt_7_1']))

        layers.append(UnPool2d(**self.layer_params['up_8']))
        layers.append(ConvT2d(weight_init=self.weight_init, **self.layer_params['convt_8_1']))
        self.decoder = layers

    def set_layer_op(self, method="AVG", num_prev_last_conv_output_channels=1, *args, **kwargs):
        if num_prev_last_conv_output_channels > 1:
            self.layer_params = update(self.layer_params, {"convt_8_1": {"output_channels":
                                                                             num_prev_last_conv_output_channels}})
        if method == "CONV":
            self.layer_params = update(self.layer_params, {"convt_8_1": {"act_fn": self.act_fn,
                                                                     "act_leak_prob": self.act_leak_prob}})
        super(SmallNetwork, self).set_layer_op(method=method, *args, **kwargs)


class SmallNetworkwKerasDecoder(SmallNetwork):

    encoder_map = {"densenet121": DenseNet121, "densenet169": DenseNet169, "densenet201": DenseNet201,
                   "incresv2": InceptionResNetV2, "incv3": InceptionV3, "mbnet": MobileNet, "mbnetv2": MobileNetV2,
                   "nasnet": NASNetLarge, "resnet50": ResNet50, "vgg16": VGG16, "vgg19": VGG19, "xception": Xception}

    def __init__(self, encoder_model_key="resnet50", layer_params=None, **kwargs):
        updated_layer_params = {"up_6": {"add_to_input": False},
                                "up_7": {"add_to_input": False},
                                "up_8": {"add_to_input": False}}
        if layer_params:
            layer_params = update(updated_layer_params, layer_params)
        else:
            layer_params = updated_layer_params
        self.encoder_model_key = encoder_model_key
        super(SmallNetworkwKerasDecoder, self).__init__(layer_params=layer_params, **kwargs)

    def init_encoder(self, encoder_layer_name=None, **kwargs):
        # have to multiply input image for 3 channels for ImageNet models
        self.inputs = tf.concat([self.inputs, self.inputs, self.inputs], axis=-1)
        # tensor has to be added to keras model so graph isn't duplicated
        # weights are hard-coded to be random, don't want to deal with pre-trained being clobbered during initialization
        # http://zachmoshe.com/2017/11/11/use-keras-models-with-tf.html
        base_model = self.encoder_map[self.encoder_model_key](weights=None, include_top=False, input_tensor=self.inputs)
        if encoder_layer_name:
            layers = {l.name: l.output for l in base_model.layers}
            self.encoder = layers[encoder_layer_name]
        else:
            self.encoder = base_model

    def encode(self, *args, **kwargs):
        return self.encoder

    def decode(self, net, center=False, unpooling_method="MAX", dp_rate=0.0):
        for i, layer in enumerate(self.decoder, start=1):
            net = layer.create_layer(net, is_training=self.is_training, center=center,
                                     unpooling_method=unpooling_method, dp_rate=dp_rate)
            self.description += "{}".format(layer.get_description())
            self.layer_outputs.append(net)
        return net
