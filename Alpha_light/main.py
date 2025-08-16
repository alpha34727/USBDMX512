from pyftdi.serialext import serial_for_url
import time

# FTDI URL 可透過 'ftdi://ftdi:232h/1' 自動搜尋，也可用 'ftdi:///1' 抓第一個
FTDI_URL = 'ftdi://ftdi:232/1'  # 若不確定，可先用 ftdi_urls() 尋找

def read_dmx_from_ftdi():
    try:
        # 開啟 FTDI UART 模式，250000 baud, 8N2 (DMX 標準)
        ser = serial_for_url(FTDI_URL, baudrate=250000,
                             bytesize=8, parity='N', stopbits=2, timeout=1)

        print("開始接收 DMX512 資料... (按 Ctrl+C 中止)")

        while True:
            data = ser.read(513)  # 1 byte start code + 最多 512 channels
            if data:
                print(f"Start Code: {data[0]}")
                for i in range(1, min(len(data), 513)):
                    print(f"Channel {i}: {data[i]}")
                print("-" * 40)
            else:
                print("等待資料中...")
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n使用者中斷")
    except Exception as e:
        print(f"錯誤：{e}")

if __name__ == "__main__":
    read_dmx_from_ftdi()
