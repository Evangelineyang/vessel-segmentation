"""This is the file for the DSA network subclass"""
from network.large_network_wo_masks import LargeNetworkWoMasks


class DsaNetwork(LargeNetworkWoMasks):

    IMAGE_WIDTH = 1024
    IMAGE_HEIGHT = 1024

    FIT_IMAGE_WIDTH = 1024
    FIT_IMAGE_HEIGHT = 1024

    def __init__(self, layers=None, skip_connections=True, **kwargs):
        super(DsaNetwork, self).__init__(layers=layers, skip_connections=skip_connections, **kwargs)