
from enum import Enum
import struct

class MessageType(Enum):

    # Time messages
    TimeStamp = 'T'
    # Reference Data Messages
    OrderBookDirectory = 'R'
    CombinationOrderBookLeg = 'M'
    TickSizeTable = 'L'
    # Event and State Change Messages
    SystemEvent = 'S'
    OrderBookState = 'O'
    # Market by Order Messages
    AddOrder = 'A'
    AddOrderWithMPID = 'F'
    OrderExecuted = 'E'
    OrderExecutedWithPrice = 'C'
    OrderReplace = 'U'
    OrderDelete = 'D'
    # Trade Messages
    Trade = 'P'
    EquilibriumPrice = 'Z'

    # Not applicable in bist
    # OrderCancel = 'X' (not in bist)
    # CrossTrade = 'Q'
    # BrokenTrade = 'B'
    # NetOrderImbalance = 'I'
    # RetailInterestMessage = 'N'
    # StockTradingAction             =  'H'
    # RegSHORestriction              =  'Y'

class Field(object):
    CrossPrice               = "CrossPrice"
    CrossType                = "CrossType"
    CurrentReferencePrice    = "CurrentReferencePrice"
    EventCode                = "EventCode" #
    FarPrice                 = "FarPrice"
    FinancialStatus          = "FinancialStatus"
    ImbalanceDirection       = "ImbalanceDirection"
    ImbalanceShares          = "ImbalanceShares"
    InterestFlag             = "InterestFlag"
    MessageType              = "MessageType" #
    MarketCategory           = "MarketCategory"
    MarketMakerMode          = "MarketMakerMode"
    MarketParticipantState   = "MarketParticipantState"
    MatchNum                 = "MatchNum"
    Mpid                     = "Mpid"
    NanoSeconds              = "NanoSeconds" #
    NearPrice                = "NearPrice"
    NewOrderRefNum           = "NewOrderRefNum"
    OrderBookID              = "OrderBookID" #
    OrderRefNum              = "OrderRefNum"
    Price                    = "Price"
    PriceFrom                = "PriceFrom" #
    PriceTo                  = "PriceTo" #
    Printable                = "Printable"
    PriceVariationIndicator  = "PriceVariationIndicator"
    PairedShares             = "PairedShares"
    PrimaryMarketMaker       = "PrimaryMarketMaker"
    Reason                   = "Reason"
    Reserved                 = "Reserved"
    RegSHOAction             = "RegSHOAction"
    RoundLotSize             = "RoundLotSize" #
    RoundLotsOnly            = "RoundLotsOnly"
    Seconds                  = "Seconds" #
    Shares                   = "Shares"
    Side                     = "Side"
    Symbol                   = "Symbol" #
    TradingState             = "TradingState"
    LongName = 'LongName' #
    ISIN = 'ISIN' #
    FinancialProduct = 'FinancialProduct' #
    Currency = 'Currency' #
    NumOfDecimals = 'NumOfDecimals' #
    NumOfDecimalsNominal = 'NumOfDecimalsNominal' #
    OddLotSize = 'OddLotSize' #
    BlockLotSize = 'BlockLotSize'
    NominalValule = 'NominalValue'
    NumOfLegs = 'NumOfLegs'
    UnderlyingOrderBookID = 'UnderlyingOrderBookID'
    StrikePrice = 'StrikePrice'
    ExpDate = 'ExpDate'
    NumOfDecimalsStrikePrice = 'NumOfDecimalsStrikePrice'
    PutOrCall = 'PutOrCall'
    CombinationOrderBookID = 'CombinationOrderBookID'
    LegOrderBookID = 'LegOrderBookID'
    LegSide = 'LegSide'
    LegRatio = 'LegRatio'
    TickSize = 'TickSize'
    StateName = 'StateName'
    OrderID = 'OrderID'
    OrderBookPosition = 'OrderBookPosition'
    Quantity = 'Quantity'
    OrderAttributes = 'OrderAttributes'
    LotType = 'LotType'
    ParticipantID = 'ParticipantID'
    ExecutedQuantity = 'ExecutedQuantity'
    MatchID = 'MatchID'
    ComboGroupID = 'ComboGroupID'
    TradePrice = 'TradePrice'
    OccuredAtCross = 'OccuredAtCross'
    NewOrderBookPosition = 'NewOrderBookPosition'
    BidQuantityAtEquilibrium = 'BidQuantityAtEquilibrium'
    AskQuantityAtEquilibrium = 'AskQuantityAtEquilibrium'
    EquilibriumPrice = 'EquilibriumPrice'
    BestBidPrice = 'BestBidPrice'
    BestAskPrice = 'BestAskPrice'
    BestBidQuantity = 'BestBidQuantity'
    BestAskQuantity = 'BestAskQuantity'



class ItchMessageFactory:
    @staticmethod
    def createFromArgs( messageArgs ):
        messageType = messageArgs[0]
        message = ItchMessageFactory.fromMessageType( messageType )
        message.fromArgs(messageArgs)
        return message

    @staticmethod
    def fromMessageType( messageType ):
        for subClass in ItchMessage.__subclasses__():
            if subClass.__name__ == messageType.name:
                return subClass()
            for subClass2 in subClass.__subclasses__():
                if subClass2.__name__ == messageType.name:
                    return subClass2()
        return None

    @staticmethod
    def createFromBytes(rawMessage):
        raw = chr( rawMessage[2] )
        msg = MessageType( raw )
        message = ItchMessageFactory.fromMessageType( msg )
#        message.MessageType = chr( rawMessage[2] )
        message.fromBytes(rawMessage)
        return message

class ItchMessage:
    def __init__(self):
        self.specs = [ ]
        self.specs.append( [ 0, 1, str, Field.MessageType ] )

    def isPriceField(self, field):
        if field == Field.Price    or field == Field.CrossPrice or \
           field == Field.FarPrice or field == Field.NearPrice  or \
           field == Field.CurrentReferencePrice:
            return True
        return False

    def fromArgs(self, args):
        self.messageLength = self.specs[len(self.specs)-1][0] + self.specs[len(self.specs)-1][1]
        endianStyle = 'big'

        self.rawMessage = bytearray()
        self.rawMessage.extend( self.messageLength.to_bytes(2, byteorder=endianStyle))
        self.rawMessage.extend( self.MessageType.encode() )
        counter = 0
        for spec in self.specs[1:]:
            val = args[1][ spec[3] ]
            if spec[2] is int:
                self.__setattr__(spec[3], val)
                if spec[1] == 4:
                    if type( val ) is float:
                        val *= 10000
                        val = int( val )
                    byteVer = ( val ).to_bytes(4, byteorder=endianStyle)
                elif spec[1] == 8:
                    byteVer = ( val ).to_bytes(8, byteorder=endianStyle)
                self.rawMessage.extend( byteVer )
            elif spec[2] is str:
                if type( val ) is MessageType:
                    byteVer = str( val.value ).encode()
                    self.__setattr__(spec[3], val.value)
                else:
                    strValue = val
                    if spec[3] == Field.Symbol:
                        strValue = val + (8 - len( val ) ) * ' '
                    elif spec[3] == Field.Mpid:
                        strValue = val + (4 - len( val ) ) * ' '
                    self.__setattr__(spec[3], val)
                    byteVer = str( strValue ).encode()
                self.rawMessage.extend( byteVer )
            counter += 1

    def fromBytes(self, rawBytesWithLen):
        self.rawMessage = rawBytesWithLen
        messageLength = struct.unpack("!h", self.rawMessage[0:2])[0]
        #self.MessageType = MessageType.SystemEvent.value
        for spec in self.specs:
            rawBytes = self.rawMessage[ 2 + spec[0] : 2 + spec[0] + spec[1] ]

            if spec[2] is int:
                if spec[1] == 2:
                    dispVal = struct.unpack("!h", rawBytes)[0]
                elif spec[1] == 4:
                    dispVal = struct.unpack("!i", rawBytes)[0]
                    if spec[3] == Field.Price:
                        dispVal /= 1000
                elif spec[1] == 8:
                    dispVal = struct.unpack("!q", rawBytes)[0]
                self.__setattr__(spec[3], dispVal)
            elif spec[2] is str:
                dispVal = rawBytes.decode()
                if spec[3] == Field.MessageType:
                    dispVal = MessageType(dispVal)
                    self.__setattr__(spec[3], self.MessageType)
                elif spec[3] == Field.Symbol:
                    self.__setattr__(spec[3], dispVal.strip())
                else:
                    self.__setattr__(spec[3], dispVal)

    def dumpRawBytes(self):
        print("--- Dumping raw message bytes ---")
        print("--  Length of payload: {0}".format(len(self.rawMessage)))
        lineLen = 8
        conv = [ "{0:#0{1}x}".format(x, 4) for x in self.rawMessage ]
        line = "\n\t- ".join( [ " ".join( conv[i:i+lineLen] ) for i in range(0, len(conv), lineLen) ] )
        print("\t- {0}".format(line))

    def dumpPretty(self):
        print("--- Pretty Dump")
        messageLength = struct.unpack("!h", self.rawMessage[0:2])[0]
        print("--- Length of message: {}".format(messageLength))
        for spec in self.specs:
            rawBytes = self.rawMessage[ 2 + spec[0] : 2 + spec[0] + spec[1] ]

            if spec[2] is int:
                if spec[1] == 2:
                    dispVal = struct.unpack("!h", rawBytes)[0]
                elif spec[1] == 4:
                    dispVal = struct.unpack("!i", rawBytes)[0]
                    if spec[3] == Field.Price:
                        dispVal /= 1000
                elif spec[1] == 8:
                    dispVal = struct.unpack("!q", rawBytes)[0]
            elif spec[2] is str:
                dispVal = rawBytes.decode()
                if spec[3] == Field.MessageType:
                    dispVal = MessageType(dispVal)
            convRawBytes = [ "{0:#0{1}x}".format(x, 4) for x in rawBytes ]
            convRawBytes = "".join( [ " ".join( convRawBytes[i:i+8] ) for i in range(0, len(convRawBytes), 8) ] )
            print("\t {:<15} : {:<20} [{}]".format(spec[3], dispVal, convRawBytes))

    def appendToFile(self, fileName=None):
        self.saveToFile('ab', fileName)

    def saveToFile(self, openMode='ab', fileName=None):
        if fileName is None:
            fileName = self.type + ".itch"
            print("Setting file name to: {0}".format(fileName))
        print("Saving to file: {0}".format(fileName))
        dataLen = len(self.rawMessage[2:])
        rawArray = bytearray(self.rawMessage[2:])
        print("Data length: {0}".format(dataLen))

        fileOut = open(fileName, openMode)
        fileOut.write(struct.pack(">H", dataLen))
        fileOut.write(rawArray)
        fileOut.close()

    def getValue(self, fieldName):
        for spec in self.specs:
            if spec[3] == fieldName:
                start = spec[0] + 2
                len = spec[1]
                if spec[2] is int:
                    #print("INT")
                    if len == 2:
                        val = struct.unpack("!h", self.rawMessage[start:start+len])[0]
                    elif len == 4:
                        val = struct.unpack("!i", self.rawMessage[start:start+len])[0]
                    elif len == 8:
                        val = struct.unpack("!q", self.rawMessage[start:start+len])[0]
                    if self.isPriceField(spec[3]):
                        val /= 1000
                elif spec[2] is str:
                    if len == 1:
                        val = struct.unpack("!c", self.rawMessage[start:start+len])[0].decode()
                    else:
                        val = self.rawMessage[start:start+len].decode().strip()
                return val
        return ""

class TimeStamp(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.TimeStamp.value
        self.specs.append( [ 1, 4, int, Field.Seconds ] )

class OrderBookDirectory(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.OrderBookDirectory.value
        self.specs.append([1, 4, int, Field.NanoSeconds])
        self.specs.append([5, 4, int, Field.OrderBookID])
        self.specs.append([9, 32, str, Field.Symbol])
        self.specs.append( [41, 32, str, Field.LongName])
        self.specs.append( [73, 12, str, Field.ISIN])
        self.specs.append( [85, 1, int, Field.FinancialProduct])
        self.specs.append([86, 3, str, Field.Currency])
        self.specs.append([89, 2, int, Field.NumOfDecimals])
        self.specs.append([91, 2, int, Field.NumOfDecimalsNominal])
        self.specs.append([93, 4, int, Field.OddLotSize])
        self.specs.append([97, 4, int, Field.RoundLotSize])
        self.specs.append([101, 4, int, Field.BlockLotSize])
        self.specs.append([105, 8, int, Field.NominalValule])
        self.specs.append([113, 1, int, Field.NumOfLegs])
        self.specs.append([114, 4, int, Field.UnderlyingOrderBookID])
        self.specs.append([118, 4, int, Field.StrikePrice])
        self.specs.append([122, 4, int, Field.ExpDate]) # Date?
        self.specs.append([124, 1, int, Field.NumOfDecimalsStrikePrice])
        self.specs.append([128, 1, int, Field.PutOrCall])

        # Notes
        # * OrderBookID: Expired Order book IDs may be reused for new instruments.
        # * NumOfDecimals: A value of 256 means that the instrument is traded in fractions (each fraction is 1/256).
        # * OddLotSize: A value of 0 indicates that this lot type is undefined for the order book.
        # * BlockLotSize: A value of 0 indicates that this lot type is undefined for the order book.
        # * PutOrCall: A value of 0 indicates that Put or Call is undefined for the order book.
        # 1 = Call
        # 2 = Put
        #
        # * Financial Product:
        # 1 = Option
        # 2 = Forward
        # 3 = Future
        # 4 = FRA
        # 5 = Cash
        # 6 = Payment
        # 7 = Exchange Rate
        # 8 = Interest Rate Swap
        # 9 = REPO
        # 10 = Synthetic Box Leg / Reference
        # 11 = Standard Combination
        # 12 = Guarantee
        # 13 = OTC General
        # 14 = Equity Warrant
        # 15 = Security Lending
        # 18 = Certificate

class CombinationOrderBookLeg(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.CombinationOrderBookLeg.value
        self.specs.append([1, 4, int, Field.NanoSeconds])
        self.specs.append([5, 4, int, Field.CombinationOrderBookID])
        self.specs.append([9, 4, int, Field.LegOrderBookID])
        self.specs.append([13, 1, str, Field.LegSide])
        self.specs.append([14, 4, int, Field.LegRatio])

        #Notes:
        # * LegSide:
        # B = As Defined
        # C = Opposite

class TickSizeTable(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.TickSizeTable.value
        self.specs.append([1, 4, int, Field.NanoSeconds ] )
        self.specs.append([5, 4, int, Field.OrderBookID ] )
        self.specs.append([9, 8, int, Field.Price])
        self.specs.append([17, 4, int, Field.PriceFrom])
        self.specs.append([21, 4, int, Field.PriceTo])

class SystemEvent(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.SystemEvent.value
        self.specs.append( [ 1, 4, int, Field.NanoSeconds ] )
        self.specs.append( [ 5, 1, str, Field.EventCode ] )
    # System Event Codes - Daily
    # 'O' - Start of Messages
    # 'S' - Start of System hours
    # 'Q' - Start of Market hours
    # 'M' - End of Market hours
    # 'E' - End of System hours
    # 'C' - End of Messages

    # System Event Codes - As Needed
    # 'A' - Emergency Market Condition - Halt
    # 'R' - Emergency Market Condition - Quote Only Period
    # 'B' - Emergency Market Condition - Resumption

class OrderBookState(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.OrderBookState.value
        self.specs.append([1, 4, int, Field.NanoSeconds])
        self.specs.append([5, 4, int, Field.OrderBookID])
        self.specs.append([9, 20, str, Field.StateName])

class AddOrder(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.AddOrder.value
        self.specs.append([1, 4, int, Field.NanoSeconds])
        self.specs.append([5, 8, int, Field.OrderID])
        self.specs.append([13, 4, int, Field.OrderBookID])
        self.specs.append([17, 1, str, Field.Side])
        self.specs.append([18, 4, int, Field.OrderBookPosition])
        self.specs.append([22, 8, int, Field.Quantity])
        self.specs.append([30, 4, int, Field.Price])
        self.specs.append([34, 2, int, Field.OrderAttributes])
        self.specs.append([36, 1, int, Field.LotType])

class AddOrderWithMPID(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.AddOrderWithMPID.value
        self.specs.append([1, 4, int, Field.NanoSeconds])
        self.specs.append([5, 8, int, Field.OrderID])
        self.specs.append([13, 4, int, Field.OrderBookID])
        self.specs.append([17, 1, str, Field.Side])
        self.specs.append([18, 4, int, Field.OrderBookPosition])
        self.specs.append([22, 8, int, Field.Quantity])
        self.specs.append([30, 4, int, Field.Price])
        self.specs.append([34, 2, int, Field.OrderAttributes])
        self.specs.append([36, 1, int, Field.LotType])
        self.specs.append([37, 7, str, Field.ParticipantID])

class OrderExecuted(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.OrderExecuted.value
        self.specs.append([1, 4, int, Field.NanoSeconds])
        self.specs.append([5, 8, int, Field.OrderID])
        self.specs.append([13, 4, int, Field.OrderBookID])
        self.specs.append([17, 1, str, Field.Side])
        self.specs.append([18, 8, int, Field.ExecutedQuantity])
        self.specs.append([26, 8, int, Field.MatchID])
        self.specs.append([34, 4, int, Field.ComboGroupID])

class OrderReplace(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.OrderReplace.value
        self.specs.append([1, 4, int, Field.NanoSeconds])
        self.specs.append([5, 8, int, Field.OrderID])
        self.specs.append([13, 4, int, Field.OrderBookID])
        self.specs.append([17, 1, str, Field.Side])
        self.specs.append([18, 4, int, Field.NewOrderBookPosition])
        self.specs.append([22, 8, int, Field.Quantity])
        self.specs.append([30, 4, int, Field.Price])
        self.specs.append([34, 2, int, Field.OrderAttributes])

class OrderDelete(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.OrderDelete.value
        self.specs.append([1, 4, int, Field.NanoSeconds])
        self.specs.append([5, 8, int, Field.OrderID])
        self.specs.append([13, 4, int, Field.OrderBookID])
        self.specs.append([17, 1, str, Field.Side])


class Trade(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.Trade.value
        self.specs.append([1, 4, int, Field.NanoSeconds])
        self.specs.append([5, 8, int, Field.MatchID])
        self.specs.append([13, 4, int, Field.ComboGroupID])
        self.specs.append([17, 1, str, Field.Side])
        self.specs.append([18, 8, int, Field.Quantity])
        self.specs.append([26, 4, int, Field.OrderBookID])
        self.specs.append([30, 4, int, Field.TradePrice])
        self.specs.append([48, 1, int, Field.Printable])

class EquilibriumPrice(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.EquilibriumPrice.value
        self.specs.append([1, 4, int, Field.NanoSeconds])
        self.specs.append([5, 4, int, Field.OrderBookID])
        self.specs.append([9, 8, int, Field.BidQuantityAtEquilibrium])
        self.specs.append([17, 8, int, Field.AskQuantityAtEquilibrium])
        self.specs.append([25, 4, int, Field.EquilibriumPrice])
        self.specs.append([29, 4, int, Field.BestBidPrice])
        self.specs.append([33, 4, int, Field.BestAskPrice])
        self.specs.append([37, 8, int, Field.BestBidQuantity])
        self.specs.append([45, 8, int, Field.BestAskQuantity])

