from abc import ABC, abstractmethod
from das_iboot.device import BootloaderDevice


class AbstractLoader(ABC):

    @abstractmethod
    def load(self, device: BootloaderDevice): ...
