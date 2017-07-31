import requests
import uuid


class CloudDevice(object):
    """Represents a TPLink cloud device."""
    def __init__(self, kwargs):
        self.id = kwargs.get('deviceId')
        self.alias = kwargs.get('alias')
        self.hardware_id = kwargs.get('hwId')
        self.hardware_version = kwargs.get('deviceHwVs')
        self.server_url = kwargs.get('appServerUrl')
        self.mac_address = kwargs.get('deviceMac')
        self.model = kwargs.get('deviceModel')
        self.name = kwargs.get('deviceName')
        self.type = kwargs.get('deviceType')
        self.firmware_id = kwargs.get('fwId')
        self.firmware_version = kwargs.get('fwVer')
        self.is_same_region = kwargs.get('isSameRegion')
        self.oem_id = kwargs.get('oemId')
        self.role = kwargs.get('role')
        self.status = kwargs.get('status')


class CloudClient(object):
    """TPCloud client."""

    def __init__(self,
                 username,
                 password,
                 url="https://wap.tplinkcloud.com",
                 ):
        self.username = username
        self.password = password
        self.url = url
        self.uuid = str(uuid.uuid4())
        self.token = self._get_token()

    def _get_token(self):
        """Get token to use on next requests."""
        data = {
            "method": "login",
            "params": {
                "appType": "Kasa_Android",
                "cloudUserName": self.username,
                "cloudPassword": self.password,
                "terminalUUID": self.uuid
            }
        }
        response = requests.post(self.url, json=data)
        assert response.status_code == 200, response
        data = response.json()
        assert data['error_code'] == 0, data
        return data['result']['token']

    def _request(self, data):
        """Send request to TPLink API"""
        url = self.url + '?token={}'.format(self.token)
        response = requests.post(url, json=data)
        assert response.status_code == 200, response
        data = response.json()
        assert data['error_code'] == 0, data
        return data.get('result')

    def get_device_list(self):
        """Return devices from this user."""
        data = {"method": "getDeviceList"}
        response = self._request(data)
        deviceList = response.get('deviceList')
        return [CloudDevice(device) for device in deviceList]