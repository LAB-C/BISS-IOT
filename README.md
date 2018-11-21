# BISS-IOT

## Basic Concept
![concept](./assets/concept.jpg)

## Usage

### 1. Run install.sh
	chmod +x install.sh && sudo ./install.sh
- Install dependencies

>caver-js,nodejs,arduino,arduino-sketch 

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
    "klaytn-node": "http://Serveraddress:8551/",
    "firmware-server": "http://Serveraddress:5000/"
}
```

- Register to server(POST json to `/api/register`)

## 2. Check server API with interval

- Send device wallet in `/api/check/update`
- (If update is available) Get `txHash`, `file_id`

## 3. public URL을 구하기

- Get `key`
- Auth to server
- Get public URL
