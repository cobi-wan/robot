# boot.py needs to be fully uncommented before running this file. Be sure to comment out all code before pushing to help other helper functions
from boot import sta_if
import ubinascii

if __name__ == "__main__":
    MAC_ADDRESS = sta_if.config('mac')
    MAC_ADDRESS = ubinascii.hexlify(MAC_ADDRESS).decode()
    print("The MAC address of this device is:", MAC_ADDRESS)