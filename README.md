# BISS-IOT

## 1. Set client name & wallet
    sudo install.sh

- Install dependencies
- Generate `info.json`
    - `device`: Device infomation
        - `name`: Used in device identification
        - `wallet`: Device Klaytn wallet address
    - `klaytn-node`: URL of running Klaytn node
    - `firmware-server`: URL of running [Firmware-server](https://github.com/junhoyeo/BISS-FirmwareServer)

```json
// info.json
{
    "device": {
        "name": "somedevice1",
        "wallet": "0x75a59b94889a05c03c66c3c84e9d2f8308ca4abd"
    },
    "klaytn-node": "http://ubuntu.hanukoon.com:8551/",
    "firmware-server": "http://ubuntu.hanukoon.com:5000/"
}
```

- Register to server(POST to `/upload`)

## 2. Check server API with interval

- Send device wallet in `/check/update`

## 3. If `Update available`
pass
