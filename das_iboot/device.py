import usb1
import re


class DeviceInvalid(Exception):
    pass


class Device(object):
    DEVICE_SERIAL_REGEX = re.compile(r"CPID:(\d{4}) CPRV:(\d{2}) CPFM:(\d{2}) SCEP:(\d{2}) BDID:([0-9A-F]{2}) "
                                     r"ECID:([0-9A-F]{16}) IBFL:([0-9A-F]{2}) SRTG:\[(.+)\]")

    CHIP_FUSE_SECURE = 0x01
    CHIP_FUSE_PRODUCTION = 0x02

    IBOOT_FLAG_IMG4 = 0x04
    IBOOT_FLAG_SECURE = 0x08
    IBOOT_FLAG_PRODUCTION = 0x1
    IBOOT_FLAG_SHA384 = 0x20

    def __init__(self, usb_device: usb1.USBDevice):
        self.usb_device = usb_device
        device_details = Device.DEVICE_SERIAL_REGEX.match(usb_device.getSerialNumber())

        if device_details is None:
            raise DeviceInvalid()

        self.chip_id = int(device_details[1])
        self.chip_revision = int(device_details[2])
        self.chip_fuse_mode = int(device_details[3])
        self.security_epoch = int(device_details[4])
        self.board_id = int(device_details[5], 16)
        self.exclusive_chip_id = device_details[6]
        self.iboot_flags = int(device_details[7], 16)
        self.iboot_version = device_details[8]

    @property
    def is_production(self) -> bool:
        return (self.chip_fuse_mode & Device.CHIP_FUSE_PRODUCTION) != 0

    @property
    def is_secure(self) -> bool:
        return (self.chip_fuse_mode & Device.CHIP_FUSE_SECURE) != 0


class BootloaderDevice(Device):
    def copy_memory_in(self, memory, preferred_address=None) -> int:
        pass

    def set_instruction_pointer(self, ip: int):
        pass
