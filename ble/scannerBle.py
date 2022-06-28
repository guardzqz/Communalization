import asyncio
import socket

from bleak import discover
import time
from bleak import BleakScanner, BleakClient
alreadyFound = []


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    print("{0}: {1}".format(sender, data))
sucess = []
fail = []
failConect = []
async def main():
    devices = await discover()
    for d in devices:
        if d.address not in alreadyFound and d.name and d.metadata['uuids']:
            print(d.address, d.name, d.metadata['uuids'])
            alreadyFound.append(d.address)
            if d.name in ['ID207 mini']:  # ID205G
                try:
                    '''连接设备'''
                    async with BleakClient(d.address, timeout=60000) as client:
                        print(f"Connected: {client.is_connected}")
                        paired = await client.pair(protection_level=1)
                        print(f"Paired: {paired}")
                        print('mtu_size', client.mtu_size)
                        try:
                            '''尝试获取回传'''
                            await client.start_notify('00000af7-0000-1000-8000-00805f9b34fb', notification_handler)
                            print('start_notify')
                            x = await client.read_gatt_char('00000af7-0000-1000-8000-00805f9b34fb')
                            print('初始获取数据', x.hex())
                            sucess.append(d)
                        except Exception as e:
                            print(e)
                            fail.append(d)
                        finally:
                            stopnotity = await client.stop_notify('00000af7-0000-1000-8000-00805f9b34fb')
                            print('stop notify', stopnotity)
                            nopaired = await client.unpair()
                            print(f'NoPaired: {nopaired}')
                            y = await client.disconnect()
                            print('disconnected', y)
                except Exception as e:
                    print('完全没连上的', e)
                    failConect.append(d)



if __name__ == "__main__":
    while True:
        asyncio.run(main())
        print('sucess', len(sucess), sucess)
        print('fail', len(fail), fail)
        print('notconnect', len(failConect), failConect)
        time.sleep(6)