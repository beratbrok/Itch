#!/usr/local/bin/python3
# /usr/local/bin/env python3
from lob_bs import *
from lob import *
import time
import dill as pickle
import os
import sys
start_time = time.time()

filename = sys.argv[1]
print(filename)

os.chdir('../moldDump')

# thelob = lob_bs('GARAN.E', '/Users/hrn/pyITCH/20170920i1p1.itch')
thelob = lob('GARAN.E', filename)

print("--- %s seconds ---" % (time.time() - start_time))
with open("/Users/canaltinigne/Desktop/pyITCH/lob_GARAN_20170920.pkl", "wb") as f:
    pickle.dump(thelob, f, pickle.HIGHEST_PROTOCOL)




# print(thelob.order_to_time_stamp)
