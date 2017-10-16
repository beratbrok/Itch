from Itch41 import *

class lob(object):
    def __init__(self,ticker, fileName):
        self.tickerMessages = {}
        self.seconds = 0
        self.last_ptr = 0
        self.id = self.__find_orderbook_id(ticker,fileName)

    def __find_orderbook_id(self,ticker, fileName):
        cacheSize = 1024 * 1024
        fin = open(fileName, "rb")
        buffer = fin.read(cacheSize)
        # print("buffer:", buffer)
        bufferLen = len(buffer)
        ptr = 0
        haveData = True
        while haveData:
            byte = buffer[ptr:ptr + 1]
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
                length = ord(buffer[ptr:ptr + 1])
                ptr += 1
                if (ptr + length) > bufferLen:
                    temp = buffer[ptr:bufferLen]
                    buffer = temp + fin.read(cacheSize)
                    bufferLen = len(buffer)
                    ptr = 0
                message = buffer[ptr:ptr + length]
                ptr += length
                if chr(message[0]) == 'R':
                    preamble = struct.pack("!h", length)
                    rawMessage = preamble + message
                    itchMessage = ItchMessageFactory.createFromBytes(rawMessage)
                    #print(itchMessage.getValue(Field.OrderBookID))
                    if itchMessage.getValue( Field.Symbol) == ticker:
                        self.last_ptr=ptr
                        return itchMessage.getValue( Field.OrderBookID)
                elif chr(message[0]) == 'A':
                    return(None)


                if ptr == bufferLen:
                    ptr = 0
                    buffer = fin.read(cacheSize)
                    bufferLen = len(buffer)
        fin.close()

    def __process_ADE_messages(self, ItchMessage):
        ItchMessage.getValue(Field.MessageType) in 'ADE'


