import asyncio
import socket, select
import time

from bleak import BleakScanner, BleakClient

from Logs.log import Loggings

from lib.getConfig import getConfig

LOG = Loggings()
class ble:
    '''连接ble'''
    def __init__(self, mac):
        LOG.info('连接ble设备', mac)
        self.macaddr = mac

    async def inBle(self, loop):
        while True:
            '''扫描设备'''
            device = await BleakScanner.find_device_by_address(self.macaddr, timeout=10)
            if not device:
                LOG.info(f'A device with address {self.macaddr} could not be found.')
            else:
                LOG.info(device)
                '''连接设备'''
                async with BleakClient(device, loop=loop, timeout=600000) as client:
                    LOG.info(f"Connected: {client.is_connected}")
                    paired = await client.pair(protection_level=1)
                    LOG.info(f"Paired: {paired}")
                    LOG.info('mtu_size', client.mtu_size)
                    ser = await client.get_services()
                    for service in ser:
                        print(service)
                        for i in service.characteristics:
                            print('\t', i, i.properties)
                    try:
                        '''尝试获取回传'''
                        await client.start_notify('00000af7-0000-1000-8000-00805f9b34fb', self.notification_handler)
                        LOG.info('start_notify')
                        x = await client.read_gatt_char('00000af7-0000-1000-8000-00805f9b34fb')
                        LOG.info('初始获取数据', x.hex())
                        '''打开socket客户端'''
                        ip_port = (getConfig('ip', 'host'), int(getConfig('port', 'host')))
                        sk = socket.socket()  # 创建套接字
                        sk.bind(ip_port)  # 绑定服务地址
                        sk.listen(5)  # 监听连接请求
                        connected = [sk]
                        LOG.info('启动socket服务，等待客户端连接...')
                        isRunning = True
                        while isRunning:
                            rs, ws, es = select.select(connected, [], [])
                            for r in rs:
                                if r is sk:
                                    conn, address = sk.accept()  # 等待连接，此处自动阻塞
                                    LOG.info('Got connection from', address)
                                    connected.append(conn)
                                else:
                                    try:
                                        client_data = r.recv(1024).decode()  # 接收信息
                                        disconnected = not client_data
                                    except socket.error:
                                        disconnected = True
                                    if disconnected:
                                        LOG.info(r.getpeername(), 'disconnected')
                                        connected.remove(r)
                                    else:
                                        LOG.info('开始发送数据', client_data)
                                        if client_data == 'quit':
                                            isRunning = False
                                            r.sendall('服务器要结束了'.encode())
                                            break
                                        await client.write_gatt_char('00000af6-0000-1000-8000-00805f9b34fb',
                                                                             bytes.fromhex(client_data))
                                        time.sleep(1)
                                        x = await client.read_gatt_char('00000af7-0000-1000-8000-00805f9b34fb')
                                        LOG.info('发送完数据', x.hex())
                                        r.sendall('服务器已经收到你的信息'.encode())  # 回馈信息给客户端
                    except Exception as e:
                        LOG.exception(e)
                    finally:
                        if hasattr(self, 'conn'):
                            '''结束后关闭socket和ble连接'''
                            conn.close()  # 关闭连接
                            LOG.info('关闭server')
                        stopnotity = await client.stop_notify('00000af7-0000-1000-8000-00805f9b34fb')
                        LOG.info('stop notify', stopnotity)
                        nopaired = await client.unpair()
                        LOG.info(f'NoPaired: {nopaired}')
                        y = await client.disconnect()
                        LOG.info('disconnected', y)
                        break


    def notification_handler(self, sender, data):
        """Simple notification handler which prints the data received."""
        LOG.info("{0}: {1}".format(sender, data))


if __name__ == "__main__":
    pass
    # aa = ble('F7:3F:51:1A:15:32')
    # aa = ble('F8:48:1F:0A:16:32')
    # aa = ble('F6:AB:7A:85:4E:E2')
    # aa = ble('F5:A1:21:3A:18:32')
    # aa = ble('01:B3:66:D1:7C:1D')
    aa = ble('7D:55:34:73:82:11')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(aa.inBle(loop))

