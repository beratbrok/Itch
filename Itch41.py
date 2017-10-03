
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
                        dispVal /= 10000
                elif spec[1] == 8:
                    dispVal = struct.unpack("!q", rawBytes)[0]
                self.__setattr__(spec[3], dispVal)
            elif spec[2] is str:
                dispVal = rawBytes.decode()
                if spec[3] == Field.MessageType:
                    dispVal = MessageType(dispVal)
                if spec[3] == Field.MessageType:
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
                        dispVal /= 10000
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
                        val /= 10000
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
        self.specs.append([85, 1, int, Field.RoundLotSize])
        self.specs.append([85, 1, int, Field.BlockLotSize])
        self.specs.append([85, 1, int, Field.NominalValule])
        self.specs.append([85, 1, int, Field.NumOfLegs])
        self.specs.append([85, 1, int, Field.UnderlyingOrderBookID])
        self.specs.append([85, 1, int, Field.StrikePrice])
        self.specs.append([85, 1, int, Field.ExpDate])
        self.specs.append([85, 1, int, Field.NumOfDecimalsStrikePrice])
        self.specs.append([85, 1, int, Field.PutOrCall])

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

class StockTradingAction(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.StockTradingAction.value
        self.specs.append( [  1, 4, int, Field.NanoSeconds ] )
        self.specs.append([5, 8, str, Field.Symbol])
        # Trading State
        # 'H' - Halted across all US equity markets/SROs
        # 'P' - Paused across all US equity markets/SROs (NASDA-listed securities only)
        # 'Q' - Quotation only period for cross-SRO halt or pause
        # 'T' - Trading on NASDAQ
        self.specs.append( [ 13, 1, str, Field.TradingState ] )
        self.specs.append( [ 14, 1, str, Field.Reserved] )
        self.specs.append( [ 15, 4, str, Field.Reason ] )

class RegSHORestriction(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.RegSHORestriction.value
        self.specs.append( [  1, 4, int, Field.NanoSeconds ] )
        self.specs.append([5, 8, str, Field.Symbol])
        # Reg SHO Short Sale Price TEst
        # '0' - No price test in place
        # '1' - Reg SHO Short Sale Price Test Restriction in effect
        # '2' - Reg SHO Short Sale Price Test Restriction remains in effect
        self.specs.append( [ 13, 1, str, Field.RegSHOAction ] )
 


class MarketParticipantPosition(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.MarketParticipantPosition.value
        self.specs.append( [  1, 4, int, Field.NanoSeconds ] )
        self.specs.append( [  5, 4, str, Field.Mpid ] )
        self.specs.append([9, 8, str, Field.Symbol])
        # Primary Market Maker
        # 'Y' - primary market maker
        # 'N' - non-primary market maker
        self.specs.append( [ 17, 1, str, Field.PrimaryMarketMaker] )
        # Market Maker Mode
        # 'N' - normal
        # 'P' - passive
        # 'S' - syndicate
        # 'R' - pre-syndicate
        # 'L' - penalty
        self.specs.append( [ 18, 1, str, Field.MarketMakerMode] )
        # Market Participant State
        # 'A' - Active
        # 'E' - Excused/Withdrawn
        # 'S' - Suspended
        # 'D' - Deleted
        self.specs.append( [ 19, 1, str, Field.MarketParticipantState] )

class AddOrder(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.AddOrder.value
        self.specs.append( [   1, 4, int, Field.NanoSeconds ] )
        self.specs.append( [   5, 8, int, Field.OrderRefNum ] )
        self.specs.append( [  13, 1, str, Field.Side ] )
        self.specs.append( [  14, 4, int, Field.Shares ] )
        self.specs.append([18, 8, str, Field.Symbol])
        self.specs.append( [  26, 4, int, Field.Price ] )

class AddOrderWithMPID(AddOrder):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.AddOrderWithMPID.value
        self.specs.append( [  30, 4, str, Field.Mpid ] )

class OrderExecuted(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.OrderExecuted.value
        self.specs.append( [   1, 4, int, Field.NanoSeconds ] )
        self.specs.append( [   5, 8, int, Field.OrderRefNum ] )
        self.specs.append( [  13, 4, int, Field.Shares ] )
        self.specs.append( [  17, 8, int, Field.MatchNum ] )

class OrderExecutedWithPrice(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.OrderExecutedWithPrice.value
        self.specs.append( [   1, 4, int, Field.NanoSeconds ] )
        self.specs.append( [   5, 8, int, Field.OrderRefNum ] )
        self.specs.append( [  13, 4, int, Field.Shares ] )
        self.specs.append( [  17, 8, int, Field.MatchNum ] )
        self.specs.append( [  25, 1, str, Field.Printable ] )
        self.specs.append( [  26, 4, int, Field.Price ] )

class OrderCancel(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.OrderCancel.value
        self.specs.append( [   1, 4, int, Field.NanoSeconds ] )
        self.specs.append( [   5, 8, int, Field.OrderRefNum ] )
        self.specs.append( [  13, 4, int, Field.Shares ] )

class OrderDelete(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.OrderDelete.value
        self.specs.append( [   1, 4, int, Field.NanoSeconds ] )
        self.specs.append( [   5, 8, int, Field.OrderRefNum ] )

class OrderReplace(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.OrderReplace.value
        self.specs.append( [   1, 4, int, Field.NanoSeconds ] )
        self.specs.append( [   5, 8, int, Field.OrderRefNum ] )
        self.specs.append( [  13, 8, int, Field.NewOrderRefNum ] )
        self.specs.append( [  21, 4, int, Field.Shares ] )
        self.specs.append( [  25, 4, int, Field.Price ] )

class TradeNonCross(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.TradeNonCross.value
        self.specs.append( [   1, 4, int, Field.NanoSeconds ] )
        self.specs.append( [   5, 8, int, Field.OrderRefNum ] )
        self.specs.append( [  13, 1, str, Field.Side ] )
        self.specs.append( [  14, 4, int, Field.Shares ] )
        self.specs.append([18, 8, str, Field.Symbol])
        self.specs.append( [  26, 4, int, Field.Price ] )
        self.specs.append( [  30, 8, int, Field.MatchNum ] )

class CrossTrade(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.CrossTrade.value
        self.specs.append( [   1, 4, int, Field.NanoSeconds ] )
        self.specs.append( [   5, 8, int, Field.Shares ] )
        self.specs.append([13, 8, str, Field.Symbol])
        self.specs.append( [  21, 4, int, Field.CrossPrice ] )
        self.specs.append( [  25, 8, int, Field.MatchNum ] )
        # Cross Type
        # 'O' - NASDAQ Opening Cross
        # 'C' - NASDAQ Closing Cross
        # 'H' - Cross for IPO and halted/paused securities
        # 'I' - NASDAQ Cross Network: Intraday Cross and Post-Close Cross
        self.specs.append( [  33, 1, str, Field.CrossType ] )

class BrokenTrade(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.BrokenTrade.value
        self.specs.append( [   1, 4, int, Field.NanoSeconds ] )
        self.specs.append( [   5, 8, int, Field.MatchNum ] )

class NetOrderImbalance(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.NetOrderImbalance.value
        self.specs.append( [   1, 4, int, Field.NanoSeconds ] )
        self.specs.append( [   5, 8, int, Field.PairedShares ] )
        self.specs.append( [  13, 8, int, Field.ImbalanceShares ] )
        self.specs.append( [  21, 1, str, Field.ImbalanceDirection ] )
        self.specs.append([22, 8, str, Field.Symbol])
        self.specs.append( [  30, 4, int, Field.FarPrice ] )
        self.specs.append( [  34, 4, int, Field.NearPrice ] )
        self.specs.append( [  38, 4, int, Field.CurrentReferencePrice] )
        self.specs.append( [  42, 1, str, Field.CrossType ] )
        self.specs.append( [  43, 1, str, Field.PriceVariationIndicator ] )

class RetailInterestMessage(ItchMessage):
    def __init__(self):
        super().__init__()
        self.MessageType = MessageType.RetailInterestMessage.value
        self.specs.append( [   1, 4, int, Field.NanoSeconds ] )
        self.specs.append([5, 8, str, Field.Symbol])
        self.specs.append( [  13, 1, str, Field.InterestFlag ] )

