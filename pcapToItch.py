#!/usr/bin/python3
#
#  Created by Veli Can KUPELI 2016 AUG
#  Revised by Can ALTINIGNE 2018 MAR


# To execute the code, enter the pcap file name as a command line argument
# For example:
# python3 pcapToItch.py equity_170801.pcap
# In the end, you will have equity_170801.itch

import dpkt
import os
import re
import sys

# os.chdir('./moldDump')

cfilename = sys.argv[1]
pcap_file = cfilename
mold_file = pcap_file.replace('.pcap', '.mold')
itch_file = pcap_file.replace('.pcap', '.itch')

for files in os.listdir():
    if re.match(pcap_file,files):
        filename=pcap_file
        break
# idx=0

f = open(filename, 'rb')
pcap = dpkt.pcap.Reader(f)
with open(mold_file,'wb') as out:
    for idx, [ts, buf] in enumerate(pcap):
        mold = dpkt.ethernet.Ethernet(buf).ip.data
        #idx+=1
        if mold.ulen > 28:
           out.write(mold.data)
           #pass
           # print(idx, mold.data)
        if idx%100000 ==0:
            print(idx)
f.close()
out.close()

f = open(mold_file,'rb')
g = open(itch_file,'wb')
print(sys.argv[1])

while True:
    i=0
    while True:
        session = f.read(10)
        if len(session) == 0:
            print(' success')
            os.remove(mold_file)
            g.close()
            f.close()
            sys.exit(0)
#        print('DEBUG session =', session)
        seqNumRaw = f.read(8)
        seqNum = int.from_bytes(seqNumRaw,'big')
#        print('DEBUG seq =', seqNum)
        messageCount = int.from_bytes(f.read(2),'big')
#        print('DEBUG messageCount =', messageCount)
        if messageCount == 0:
            print('DEBUG MESSAGE COUNT IS ZERO')
            continue
        else:
            for x in range(messageCount):
                messageLength = f.read(2)
                messageLengthInt = int.from_bytes(messageLength,'big')
                try:
                    cond = messageLength.decode('utf8') == 'TR'
                except UnicodeDecodeError as err:
                    cond = False
                if(cond):
                    f.seek(-2,1)
                    break
                messageType = f.read(1)
                message = f.read(messageLengthInt-1)
                g.write(messageLength)
                g.write(messageType)
                g.write(message)

print('Success')
exit(0)
