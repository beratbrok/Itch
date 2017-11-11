#!/usr/local/bin/python3
# /usr/local/bin/env python3
from lob_bs import *
import time
import dill as pickle
start_time = time.time()

thelob = lob_bs('GARAN.E', '/home/matriks/helpers/i20171101i1p1.itch')

print("--- %s seconds ---" % (time.time() - start_time))
with open("./lob_GARAN_20170920.pkl", "wb") as f:
    pickle.dump(thelob, f, pickle.HIGHEST_PROTOCOL)




# print(thelob.order_to_time_stamp)
