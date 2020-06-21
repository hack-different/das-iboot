from abc import ABCMeta, abstractmethod
from das_iboot.device import Device, BootloaderDevice


class AbstractStrategy(metaclass=ABCMeta):

    @staticmethod
    def strategy_applies(device: Device) -> bool:
        return False

    @abstractmethod
    def create_bootloader_device(self, device: Device) -> BootloaderDevice: ...
