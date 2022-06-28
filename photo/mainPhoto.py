
from Logs.log import Loggings
from lib.getConfig import getConfig
from photo.phone.OperationCamera import OperationCamera
from photo.phone.OperationScreen import OperationScreen
from photo.phone.Phonedriver import Phonedriver
from photo.usb.usbClient import usbClient


LOG = Loggings()
class mainPhoto:
    def __init__(self):
        self.method = getConfig('method', 'photo')
        if self.method == 'phone':
            Phonedriver().startApp()
        elif self.method == 'usb':
            usbClient()

    def camera(self, path, description=None):
        if self.method == 'phone':
            OperationCamera.camera(path, description)
        elif self.method == 'usb':
            usbClient.controlUsb('p', path, description)

    def recodingScreen(self):
        if self.method == 'phone':
            OperationScreen().recodingScreen()
        elif self.method == 'usb':
            usbClient.controlUsb('s')

    def killScreen(self, path, description=None):
        if self.method == 'phone':
            OperationScreen().killScreen(path, description)
        elif self.method == 'usb':
            usbClient.controlUsb('e', path, description)


if __name__ == '__main__':
    a = mainPhoto()