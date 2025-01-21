# microros

# Arduino IDE

## Windows

Follow the [link](https://learn.microsoft.com/ja-jp/windows/wsl/connect-usb)

* USBIPD install
* Share device
```bash
usbipd list # check device bus id. <busid> looks 1-1 
usbipd bind --busid  <busid>
usbipd list
```

Then state will change "Shared"

* Attach to wsl

```bash 
usbipd attach --wsl --busid <busid>
```

Then the device will appear in /dev/