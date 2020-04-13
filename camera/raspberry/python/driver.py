import serial as serial
import time as t
import struct

#https://github.com/adafruit/Adafruit-VC0706-Serial-Camera-Library/blob/master/examples/Snapshot/Snapshot.ino

ACK1 = b'\x76\x00\x31\x00\x00'
ACK4 = b'\x76\x00\x34\x00\x00'
ACK6 = b'\x76\x00\x36\x00\x00'
    
"""
set image resolution
00 = 640 x 480
11 = 320 x 240
22 = 160 x 120
"""
def resolution(s):
    s.write(b'\x56\x00\x31\x05\x04\x01\x00\x19')
    s.write(b'\x22')

    if (s.read(5) != ACK1):
        print("Failed image resolution")
        exit()

"""
set image compressibility
range between 00 to ff
"""
def compressibility(s):
    s.write(b'\x56\x00\x31\x05\x01\x01\x12\x04')
    s.write(b'\xff')

    if (s.read(5) != ACK1):
        print("Failed image compression")
        exit()

"""
reset
"""
def reset(s):
    s.write(b'\x56\x00\x26\x00')

    if (s.read(4) != b'\x76\x00\x26\x00'):
        print("Failed reset")
        exit()

"""
stop capture
"""
def stop(s):
    s.write(b'\x56\x00\x36\x01\x02')
    if (s.read(5) != ACK6):
        print("Failed stop capture")
        exit()

"""
start capture
"""
def start(s):
    s.write(b'\x56\x00\x36\x01\x00')

    if (s.read(5) != ACK6):
        print("Failed start capture")
        exit()

"""
transfer frame buffer
"""
def transfer(s):
     #read data length
    s.write(b'\x56\x00\x34\x01\x00')
    buffer = s.read(9)
    if ( buffer[0:5] != ACK4):
        print("Failed read data length")
        exit()
    len = struct.unpack("i", buffer[5:9])

    #read data
    s.write(b'\x56\x00\x32\x0C\x00\x0F\x00\x00\x00\x00')
    buffer = s.read(9)
    if ( buffer[0:5] != ACK4):
        print("Failed read data length")
        exit()
    len = struct.unpack("i", buffer[5:9])


#If this program is the main program, one jpeg will be saved
def main():
    s = serial.Serial("/dev/ttyS0")
    s.baudrate = 38400
    s.open()
    reset(s)
    t.sleep(3)
    resolution(s)
    compressibility(s)
    start(s)
    t.sleep(1)
    stop(s)
    transfer(s)
    s.close()

if __name__ == "__main__":
    main()