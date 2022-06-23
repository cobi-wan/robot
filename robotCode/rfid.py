class RFID:
    def Rfid_tag():
        from mfrc522 import MFRC522
        from machine import SPI, Pin

        spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
        # Using Hardware SPI pins:
        #     sck=18   # yellow
        #     mosi=23  # orange
        #     miso=19  # blue
        #     rst=4    # white
        #     cs=5     # green, DS
        # *************************
        # To use SoftSPI,
        # from machine import SOftSPI
        # spi = SoftSPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
        spi.init()
        rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)
        print("Place card")

        while True:
            (stat, tag_type) = rdr.request(rdr.REQIDL)
            if stat == rdr.OK:
                (stat, raw_uid) = rdr.anticoll()
                if stat == rdr.OK:
                    #card_id = "uid: 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                    #if card_id == "uid: 0xc3e9561c":
                    print("stop")
                    return 1
                else:
                    print("go")
                    return 0
            else:
                return 0

                    
