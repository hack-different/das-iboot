from das_iboot.loader import AbstractLoader
from das_iboot.device import BootloaderDevice


class PongoLoader(AbstractLoader):
    def __init__(self, pongo_image):
        self.pongo_image = pongo_image

    def load(self, device: BootloaderDevice):
        pass
