from das_iboot.strategy import AbstractStrategy
from das_iboot.device import Device, BootloaderDevice


class Checkm8Strategy(AbstractStrategy):
    APPLICABLE_CHIP_IDS = [8010, 8012]

    @staticmethod
    def strategy_applies(device: Device) -> bool:
        return device.chip_id in Checkm8Strategy.APPLICABLE_CHIP_IDS

    def create_bootloader_device(self, device: Device) -> BootloaderDevice:
        # Somewhere in here checkm8 happens and we have control of memory and instruction pointer

        # We recreate the device and therefore will trigger a re-interrogation of the USB parameters
        return BootloaderDevice(device.usb_device)
