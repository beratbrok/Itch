#!/usr/bin/python3
#/usr/bin/env python3

import struct
from Itch41 import *
from lob import *
import struct


#### Parameters for Execution
# Download from here: ftp://emi.nasdaq.com/ITCH/11092013.NASDAQ_ITCH41.gz
fileName = "20170920i1p1.itch"
#fileName = "11092013.NASDAQ_ITCH41"
outputFile = "20170920i1p1ITCH.dat"
saveMessageTypes = [ 'A' ]
numberOfMessagesToSave = 2

#fileName = "Itch.dat"

cacheSize = 1024 *1024
fin = open(fileName, "rb")


buffer = fin.read(cacheSize)
# print("buffer:", buffer)
bufferLen = len(buffer)
# print(bufferLen)
ptr = 0
haveData = True
while haveData:
    byte = buffer[ptr:ptr+1]
    # print(byte)
    ptr += 1
    # print('ptr:', ptr)
    if ptr == bufferLen:
        ptr = 0
        buffer = fin.read(cacheSize)
    bufferLen = len(buffer)
    if len(byte) == 0:
        # print("BREAK-len(byte) == 0")
        break
    if byte == b'\x00':
        length = ord(buffer[ptr:ptr+1])
        ptr += 1
        if (ptr+length) > bufferLen:
            temp = buffer[ptr:bufferLen]
            buffer = temp + fin.read(cacheSize)
            bufferLen = len(buffer)
            ptr = 0
        message = buffer[ptr:ptr+length]
        ptr += length

        preamble = struct.pack("!h", length)
        print("preamble:", preamble)
        rawMessage = preamble + message
        print("rawMessage :", rawMessage )

        itchMessage = ItchMessageFactory.createFromBytes(rawMessage)
        # print("itchMessage: ",  itchMessage.getValue( Field.MessageType ) in 'ADC')
        # if fptr(itchMessage):
        #     break
        if itchMessage.getValue(Field.MessageType) == 'T':
            print(itchMessage.getValue(Field.Seconds))

        if ptr == bufferLen:
            ptr = 0
            buffer = fin.read(cacheSize)
            bufferLen = len(buffer)

fin.close()

