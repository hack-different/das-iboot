from typing import Dict, Protocol, Iterator
import usb1
from das_iboot.device import Device
from das_iboot.checkm8_strategy import Checkm8Strategy


class DeviceAttached(Protocol):
    def __call__(self, device: Device) -> None: ...


def strategy_for_device(device: Device):
    for strategy in [Checkm8Strategy]:
        if strategy.strategy_applies(device):
            return strategy()

    return None


class Manager(object):
    USB_APPLE_VENDOR_ID = 0x05AC
    USB_APPLE_DFU_PRODUCT_ID = 0x1227

    def __init__(self):
        self.context = usb1.USBContext()
        self.device_attach_handlers = []

        if not self.context.hasCapability(usb1.CAP_HAS_HOTPLUG):
            registration = self.context.hotplugRegisterCallback(_hot_plug_callback,
                                                                vendor_id=Manager.USB_APPLE_VENDOR_ID,
                                                                product_id=Manager.USB_APPLE_DFU_PRODUCT_ID)

            self.hot_plug_registration = registration

            hot_plug_handlers[self.context] = self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context.__exit__(exc_type, exc_val, exc_tb)

    # TODO: Need to handle cleanup of USBContext - but alas I need to read up on this disposable pattern
    #  in python before I do
    def __del__(self):
        pass

    def device_callback(self, device, event):
        if event == usb1.HOTPLUG_EVENT_DEVICE_ARRIVED:
            for handler in self.device_attach_handlers:
                handler(self._create_device(device))

    def add_device_attach_handler(self, handler: DeviceAttached):
        self.device_attach_handlers += handler

    @staticmethod
    def _create_device(device: usb1.USBDevice) -> Device:
        return Device(device)

    @staticmethod
    def _device_applicable(device: usb1.USBDevice) -> bool:
        return device.getVendorID() == Manager.USB_APPLE_VENDOR_ID and \
               device.getProductID() == Manager.USB_APPLE_DFU_PRODUCT_ID

    def devices(self):
        for device in self.context.getDeviceList():
            if Manager._device_applicable(device):
                yield Device(device)


hot_plug_handlers: Dict[usb1.USBContext, Manager] = {}


def _hot_plug_callback(context, device, event):
    hot_plug_handlers[context].device_callback(device, event)
