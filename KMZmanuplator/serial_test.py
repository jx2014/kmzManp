import time
import serial

ser = serial.Serial('COM7',
        baudrate=115200, 
        parity=serial.PARITY_NONE, 
        stopbits=serial.STOPBITS_ONE, 
        bytesize=serial.EIGHTBITS, 
        timeout=2)


n = 1000000
m = 1
while (m < n):
    m = m + 1
    ser.write("attest=1\r")
    time.sleep(0.2)
    ser.write("attest=0\r")
    time.sleep(0.1)