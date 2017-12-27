#!/usr/local/bin/python3
# /usr/local/bin/env python3
from lob_bs import *
import time
import dill as pickle
import os
start_time = time.time()
os.chdir('/home/tacirler/moldDump/')
# thelob = lob_bs('TCELL.E', 'itch_not_hearbeats2')
thelob = lob_bs('AKBNK.E', '/home/matriks/helpers/20171129p1.itch')
# thelob = lob_bs('GARAN.E', '/Users/hrn/pyITCH/20170920i1p1.itch')
# thelob = lob_bs('GARAN.E', '/home/matriks/dumps/itchDump/itch_not_hearbeats2')

print("--- %s seconds ---" % (time.time() - start_time))
with open("/home/matriks/helpers/lob_GARAN_20170920.pkl", "wb") as f:
    pickle.dump(thelob, f, pickle.HIGHEST_PROTOCOL)
f.close()

# print(thelob.order_to_time_stamp)