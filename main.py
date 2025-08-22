import hid
import time
import pprint
# from tqdm import tqdm

ALL_CH = 255


# print(len(init_dat))
# exit()

"""
byte
0  1  2  3  4  5  6  7  8  9
00 00 00 00 00 00 00 00 00 00

0~2: 時間，每次發送增加9700
6：與byte 2相同
7~8：自己互相相同
9：包起點順序，一輪中每次增加54

"""

header = [[0, 111, 184, 7, 139, 112, 142, 7, 191, 191, 0],
[0, 9, 222, 7, 142, 112, 232, 7, 217, 217, 54],
[0, 220, 4, 8, 134, 128, 50, 8, 12, 12, 108],
[0, 242, 42, 8, 136, 128, 28, 8, 34, 34, 162],
[0, 136, 80, 8, 136, 128, 102, 8, 88, 88, 216],
[0, 174, 118, 8, 135, 144, 64, 8, 126, 126, 14],
[0, 68, 156, 8, 141, 144, 170, 8, 148, 148, 68],
[0, 26, 194, 8, 139, 144, 244, 8, 202, 202, 122],
[0, 48, 232, 8, 133, 144, 222, 8, 224, 224, 176],
[0, 215, 14, 9, 142, 128, 20, 9, 7, 7, 230]]

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
    print("寫入資料")
    
    # 初始化
    print("初始化")
    # init_dat = [0xfc, 0x26, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,]
    init_dat = [0x00, 0xFC, 0x26]
    h.write(init_dat)
    h.write(init_dat)
    
    dat = [0 for x in range(540)]
    
    while (True):
        channel, val = map(int, input("通道, 數值").split(" "))
        
        dat[channel - 1] = val
        
        for i in range(10):
            tmp_dat = header[i][:]
            
            tmp_dat += dat[i*54 : (i+1) * 54]
            
            h.write(tmp_dat)
            
            for ch in tmp_dat[11:]:
                print(f"{ch:03d}", sep='', end=' ')
            
            print()
        
    
    # 嘗試傳送一輪資料
    # print("嘗試傳送一輪資料")
    # for r in tqdm(range(1)):
    #     for i in range(10):
    #         dat = header[i][:]
    #         print('Header:', header[i][:])
            
    #         for ch in range(54):
    #             dat.append(ALL_CH)
    #         h.write(dat)
    #     print("傳送成功")
    #     time.sleep(10/1000)

    # wait
    time.sleep(0.05)

    # read back the answer
    # print("Read the data")
    # while True:
    #     d = h.read(64)
    #     if d:
    #         print(d)
    #     else:
    #         break

    print("Closing the device")
    h.close()

except IOError as ex:
    print(ex)
    print("You probably don't have the hard-coded device.")
    print("Update the h.open() line in this script with the one")
    print("from the enumeration list output above and try again.")

print("Done")