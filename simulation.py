import json
import pprint
import hid
import time
from tqdm import tqdm

file_path = open('test.json', 'r', encoding='utf-8')

def pharse_to_list(urb_dat):
    dat = [0, ]
    for c in range(0, len(urb_dat), 3):
        a = int(urb_dat[c:c+2], 16)
        dat.append(a)
    return dat

try:
    # 開啟設備
    print("嘗試開啟USB-DMX512")
    h = hid.device()
    h.open(0x16C0, 0x27D9)  # VendorID/ProductID
    
    # 讀取型號
    print("型號：%s" % h.get_product_string())
    print("SN：%s" % h.get_serial_number_string())

    # enable non-blocking mode
    h.set_nonblocking(1)

    # 嘗試寫一些資料
    print("嘗試模擬")
    
    dat = json.load(file_path)
    for i in tqdm(range(len(dat))):
        # urb_data = dat[i]["_source"]["layers"].get("usb.capdata")
        urb_data = dat[i]["_source"]["layers"].get("usbhid.data")
        delay_time = float(dat[i]["_source"]["layers"]["frame"]["frame.time_delta"])
        if urb_data != None:
            pharsed_dat = pharse_to_list(urb_data)
            
            print('Send: ', pharsed_dat[1:])
            h.write(pharsed_dat)
            
            time.sleep(delay_time)
    
    print("Closing the device")
    h.close()

except IOError as ex:
    print(ex)
    print("You probably don't have the hard-coded device.")
    print("Update the h.open() line in this script with the one")
    print("from the enumeration list output above and try again.")

print("Done")