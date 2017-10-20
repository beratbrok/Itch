from Itch41 import *

global orderBook
orderBook = { }

def OrderBook(itchMessage):
    global counter
    global orderBook
    counter += 1

    ticker = "GARAN.E"

    messageType = MessageType( itchMessage.getValue( Field.MessageType ))
    if messageType == MessageType.AddOrder or messageType == MessageType.AddOrderWithMPID:
        if itchMessage.getValue( Field.Stock ) == ticker:
            orderRefNum = itchMessage.getValue(Field.OrderRefNum)
            if orderRefNum in orderBook:
                print("Already exists")
            orderBook[orderRefNum] = itchMessage
    if counter == 1500000:
        print("Number of messages in orderbook: {}".format( len(orderBook.keys() )))
        for orderRefNum in orderBook.keys():
            #orderRefNum = order.getValue(Field.OrderRefNum)
            order = orderBook[orderRefNum]
            price = order.getValue(Field.Price)
            shares = order.getValue(Field.Shares)
            #print("OrderRefNum: {}, Price: {}, Shares: {}".format( orderRefNum, price, shares))
        return True
    return False



def createUnitTestCode(message, rawBytes):
    lineLen = 8
    conv = [ "{0:#0{1}x}".format(x, 4) for x in rawBytes]
    #line = "\n\t- ".join( [ " ".join( conv[i:i+lineLen] ) for i in range(0, len(conv), lineLen) ] )
    lines = [ ", ".join( conv[i:i+lineLen] ) for i in range(0, len(conv), lineLen) ]
    print("\n\tdef test_create_{}(self):".format( MessageType(message.MessageType) ))
    print("\t\t# GIVEN")
    print("\t\trawMessage = bytearray()")
    for line in lines:
        print("\t\trawMessage.extend( [ {0} ] )".format(line))
    print("\n\t\t# WHEN")
    print("\t\tmessage = ItchMessageFactory.createFromBytes( rawMessage )")
    print("\n\t\t# THEN")
    for spec in message.specs:
        leftVal = getattr(message, spec[3])
        rightVal = "message." + spec[3]
        if spec[2] is str:
            if spec[1] == 1:
                leftVal = "'" + leftVal + "'"
            else:
                leftVal = "\"" + leftVal + "\""

        print("\t\tself.assertEqual( {:>10}, {:<30} )".format( leftVal, rightVal ))
    print("\n")

global counter
counter = 0

global uniqueCounter
uniqueCounter = { }
def dumpOneOfEach(itchMessage):
    global uniqueCounter

    messageType = MessageType( itchMessage.getValue( Field.MessageType ))
    if not messageType in uniqueCounter:
        #itchMessage.dumpPretty()
        #itchMessage.dumpRawBytes()
        createUnitTestCode( itchMessage, itchMessage.rawMessage )
        uniqueCounter[messageType] = itchMessage
    if len(uniqueCounter.keys()) == 18:
        return True
    return False

#fptr = OrderBook
fptr = dumpOneOfEach