# import machine
# import usocket as socket
# import time
# import network

# # Wifi Constants
# timeout = 0

# SSID = 'HirshPrecision'
# Password = 'H1rshHasVision!'

# # Network Initialization
# wifi = network.WLAN(network.STA_IF)

# # Wifi Reset
# wifi.active(False)
# time.sleep(0.5)
# wifi.active(True)

# # Connect to Wifi
# wifi.connect(SSID, Password)

# # Timeout Status
# if not wifi.isconnected():
#     print('Connecting..')
#     while (not wifi.isconnected() and timeout < 5):
#         print(5 - timeout)
#         timeout = timeout + 1
#         time.sleep(1)
        

# # Successful Connection Message/Status
# if(wifi.isconnected()):
#     print('Connected...')
#     print('Network Config:', wifi.ifconfig())

# # Socket Initilation
# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# Host = ''
# Port = 80
# s.bind((Host,Port))
# s.listen(5)
