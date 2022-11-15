from pyLoraRFM9x import LoRa, ModemConfig
import time
Channel = 1 #or chip to be used
ServerAddress = 1

def on_recv(payload):
    print("From:", payload.header_from)
    print("Received:", payload.message)
    print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))

lora = LoRa(Channel, 5, ServerAddress, reset_pin = 25, freq=915, modem_config=ModemConfig.Bw125Cr45Sf128, tx_power=14, acks=True)
# lora.on_recv = on_recv
#channel 1 yun, GPIO5 for interrupts

lora.set_mode_rx()


import base64
f = open("/home/pi/Desktop/Main/GUI/Video.jpg", "rb+")
x = f.read()
x = base64.b64encode(x)
lens = len(x)


f = open("Vvv.txt", "w+")
f.write(str(x)) 
f.close()
            

status = lora.send("=", 2)
if status is True:
    print("Message sent!")
else:
    print("No acknowledgment from recipient")
time.sleep(5)

for i in range(int(lens/250)+1):
    message = x[i*250:(i+1)*250]
    
    status = lora.send(message, 2)
    if status is True:
        print(i,"Message sent!", len(message))
    else:
        print("No acknowledgment from recipient")
    time.sleep(0.4)

status = lora.send("=", 2)
if status is True:
    print("Message sent!")
else:
    print("No acknowledgment from recipient")
time.sleep(5)

f.close()

lora.close()
