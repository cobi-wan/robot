class RFID:
    def __init__(self):
        from Classes.Sensors.mfrc522 import MFRC522
        from machine import SPI, Pin

        self.spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
        # Using Hardware SPI pins:
        #     sck=18   # yellow
        #     mosi=23  # orange
        #     miso=19  # blue
        #     rst=4    # white
        #     cs=21     # green, DS
        # *************************
        # To use SoftSPI,
        # from machine import SOftSPI
        # spi = SoftSPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
        self.spi.init()
        self.rdr = MFRC522(spi=self.spi, gpioRst=4, gpioCs=5)

    def checkTag(self):
        (stat, tag_type) = self.rdr.request(self.rdr.REQIDL)
        if stat == self.rdr.OK:
            print("RDR ok")
            (stat, raw_uid) = self.rdr.anticoll()
            if stat == self.rdr.OK:
                # if raw_uid == PATH[0]:
                #     PATH.pop()
                #     print("Teehee")
                #     return True
                # else:
                #     print("Toohoo")
                #     return False
                return (True, raw_uid)
            else:
                return (False, None)
        else:
            return (False, None)

                    
