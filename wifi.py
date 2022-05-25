import machine
import usocket as socket
import time
import network

# Wifi Constants
timeout = 0

SSID = 'HirshPrecision'
Password = 'H1rshHasVision!'

# Network Initialization
wifi = network.WLAN(network.STA_IF)

# Wifi Reset
wifi.active(False)
time.sleep(0.5)
wifi.active(True)

# Connect to Wifi
wifi.connect(SSID, Password)

# Timeout Status
if not wifi.isconnected():
    print('Connecting..')
    while (not wifi.isconnected() and timeout < 5):
        print(5 - timeout)
        timeout = timeout + 1
        time.sleep(1)
        

# Successful Connection Message/Status
if(wifi.isconnected()):
    print('Connected...')
    print('Network Config:', wifi.ifconfig())
    
# Website Code
html='''<!DOCTYPE html>
<html>
<center><h2>ESP32 Webserver </h2></center>
<form>
<center>
<h3> LED </h3>
<button name="LED" value='ON' type='submit'>  ON </button>
<button name="LED" value='OFF' type='submit'> OFF </button>
</center>
'''

# LED Initialization
LED = machine.Pin(2,machine.Pin.OUT)
LED.value(0)

# Socket Initilation
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Host = ''
Port = 80
s.bind((Host,Port))
s.listen(5)

# Main Loop
while True:

  # Accept Connection
  connection_socket,address=s.accept()
  print("Got a connection from ", address)

  # Store/Print HTTP Request
  request=connection_socket.recv(1024)
  print("Content:")
  print(request)
  request=str(request)

  # Search for ON/OFF Status in request and store it
  LED_ON =request.find('/?LED=ON')
  LED_OFF =request.find('/?LED=OFF')
  
  # Set LED based on request
  if(LED_ON==6):
    LED.value(1)
    
  if(LED_OFF==6):
    LED.value(0)
    
  # Reset the webpage 
  response=html 
  connection_socket.send(response)
  
  # Close the socket
  connection_socket.close()