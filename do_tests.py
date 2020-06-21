from das_iboot.manager import Manager, strategy_for_device


manager = Manager()
for device in manager.devices():
    strategy = strategy_for_device(device)
    bootloader_device = strategy.create_bootloader_device(device)
    print(bootloader_device)
