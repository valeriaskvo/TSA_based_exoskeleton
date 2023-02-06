# How to upload firmware on esp32 board
**Step 1:** Eraese flash
```
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
```

**Step 2:** Upload firmware
```
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z --flash_mode dio --flash_freq 40m 0x1000 can_esp32_firmware.bin
```

**Step 3:** Hard reboot esp32 board