from Itch41 import *
from datetime import datetime
import collections
import time

class lob(object):
    def __init__(self,ticker, fileName):
        self.fileName =fileName
        self.ob={}
        self.tickerMessages = {}
        self.order_to_time_stamp = {}
        self.seconds = 0
        self.last_ptr = 0
        self.__seconds = 0
        self.id = self.__find_orderbook_id(ticker,fileName)
        self.__process_relevant_messages()

    def find_p_and_q_from_id(self, id):
        time_stamp = self.order_to_time_stamp[id]
        p_q = [[x[-3], x[-1]] for x in self.tickerMessages[time_stamp] if x[1]==id and x[0]=='A'][0]
        print(p_q)
        return p_q

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
                    return None


                if ptr == bufferLen:
                    ptr = 0
                    buffer = fin.read(cacheSize)
                    bufferLen = len(buffer)
        fin.close()


    def __process_relevant_messages(self):
        cacheSize = 1024 * 1024
        fin = open(self.fileName, "rb")

        buffer = fin.read(cacheSize)
        # print("buffer:", buffer)
        bufferLen = len(buffer)
        # print(bufferLen)
        ptr = self.last_ptr
        haveData = True
        i=0
        while haveData:
            i+=1
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
                #ptr += length

                preamble = struct.pack("!h", length)
                # print("preamble:", preamble)
                rawMessage = preamble + message
                # print("rawMessage :", rawMessage )

                itchMessage = ItchMessageFactory.createFromBytes(rawMessage)
                ptr += length
                # print("itchMessage: ",  itchMessage.getValue( Field.MessageType ) in 'ADC')
                # if fptr(itchMessage):
                #     break
                if itchMessage.getValue(Field.MessageType) =='T':
                    self.__seconds = itchMessage.getValue(Field.Seconds)
                # print(itchMessage.getValue(Field.OrderBookID))

                if itchMessage.getValue(Field.OrderBookID) == self.id:
                    # print(itchMessage.getValue(Field.MessageType))
                    if itchMessage.getValue(Field.MessageType) in 'ADE':
                        # print(itchMessage.getValue(Field.MessageType))
                        nanotime = itchMessage.getValue(Field.NanoSeconds)
                        seconds_str = datetime.fromtimestamp(self.__seconds ) # + nanotime/1e9
                        time_stamp = seconds_str.strftime('%Y-%m-%d %H:%M:%S') + '.' + str(int(nanotime % 1000000000)).zfill(9)
                        order_id = itchMessage.getValue(Field.OrderID)
                        ob_side = itchMessage.getValue(Field.Side)
                        type = itchMessage.getValue(Field.MessageType)
                        self.ob.update({0: time_stamp})
                        # print(ob_side)
                        sign = (int('S' in ob_side) * 2) - 1

                        if type == 'D':
                            this_message = [type, order_id, ob_side]
                            quantity, price = self.find_p_and_q_from_id(order_id)
                            #print(price, ':', self.ob[price], ' - ', quantity)
                            self.ob[price] -= quantity *sign

                        elif type == 'A':
                            self.order_to_time_stamp.update({order_id:time_stamp})
                            price = itchMessage.getValue(Field.Price)
                            position = itchMessage.getValue(Field.OrderBookPosition)
                            quantity = itchMessage.getValue(Field.Quantity)
                            this_message = [type, order_id, ob_side, quantity, position, price]

                            print(quantity)
                            if price in self.ob:
                                self.ob[price] += quantity *sign
                            else:
                                self.ob.update({price:quantity*sign })

                        elif type == 'E':
                            quantity = itchMessage.getValue(Field.ExecutedQuantity)
                            match_id = itchMessage.getValue(Field.MatchID)
                            this_message = [type, order_id, ob_side, quantity, match_id]
                            price = self.find_p_and_q_from_id(order_id)[1]
                            #print(price,':', self.ob[price],' - ', quantity)
                            self.ob[price] -= quantity * sign

                        print(type, ob_side, sign, quantity)


                        if time_stamp not in self.tickerMessages:
                            self.tickerMessages.update( {time_stamp:[this_message]})
                        else:
                            self.tickerMessages.get(time_stamp).append(this_message)
                        print(collections.OrderedDict(sorted(self.ob.items())))




                if ptr == bufferLen:
                    ptr = 0
                    buffer = fin.read(cacheSize)
                    bufferLen = len(buffer)
        fin.close()