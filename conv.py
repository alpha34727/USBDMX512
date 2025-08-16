import json
import pprint
import hid
import time
from tqdm import tqdm

file_path = open('out_all255.json', 'r', encoding='utf-8')

def pharse_to_list(urb_dat):
    dat = []
    for c in range(0, len(urb_dat), 3):
        a = int(urb_dat[c:c+2], 16)
        dat.append(a)
    return dat

dat = json.load(file_path)

it = 0
for i in (range(len(dat))):
    # urb_data = dat[i]["_source"]["layers"].get("usb.capdata")
    urb_data = dat[i]["_source"]["layers"].get("usbhid.data")
    delay_time = float(dat[i]["_source"]["layers"]["frame"]["frame.time_delta"])
    relative_time = float(dat[i]["_source"]["layers"]["frame"]["frame.time_relative"])
    time_epoch = float(dat[i]["_source"]["layers"]["frame"]["frame.time_epoch"])
    if urb_data != None:
        pharsed_dat = pharse_to_list(urb_data)
        # output = (pharsed_dat[2] << 16) + (pharsed_dat[1] << 8) + (pharsed_dat[0] << 0)
        # output = pharsed_dat[7] + 255 * (it // 7)
        # output = pharsed_dat[9]
        # output = (pharsed_dat[4] << 8) + (pharsed_dat[3] << 0)
        # output = (pharsed_dat[3])
        # print(it, output, sep=',', end='\n')
        print(pharsed_dat[0:10])
        it += 1 