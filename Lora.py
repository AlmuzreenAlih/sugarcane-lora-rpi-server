import base64
from pyLoraRFM9x  import LoRa, ModemConfig
import time
class MyTimer:
    def __init__(self):
        self.StartTime = 0
        self.TargetTime = 0
        self.Force = 0
    
    def start(self, TargetTime):
        self.Force = 0
        self.StartTime = time.time()
        self.TargetTime = TargetTime
        
    def justFinished(self):
        # print(self.Force,time.time()-self.StartTime, self.TargetTime)
        if self.Force == 1:
            return False
        if (time.time()-self.StartTime > self.TargetTime):
            self.Force = 1
            return True
        else:
            return False
    def elapsed(self):
        return time.time()-self.StartTime

Timer1 = MyTimer()

Channel = 1 #or chip to be used
ServerAddress = 2
ClientAddress = 10
Data_Recv = ""
def on_recv(payload):
    global Data_Recv
    Data_Recv = payload.message
    # print("From:", payload.header_from)
    # print("Received:", Data_Recv)
    # print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))

lora = LoRa(Channel, 5, ServerAddress, reset_pin = 25, freq=915, modem_config=ModemConfig.Bw125Cr45Sf128, tx_power=14, acks=True)
lora.on_recv = on_recv
#channel 1 yun, GPIO5 for interrupts

lora.set_mode_tx()

f = open("/home/pi/Desktop/Main/GUI/Video.jpg", "rb+")
file_bytes = f.read()
file_bytes = base64.b64encode(file_bytes)
lens = len(file_bytes)
length = 248

##HEADER SENDING
retries = 0          
while True:
    status = lora.send("=", ClientAddress)
    if status is True:
        print("Header sent!")
    else:
        print("none")
    Timer1.start(3)
    Data_Recv2 = ""
    while True:
        if Data_Recv != "":
            try:
                Data_Recv2 = Data_Recv[0:1].decode('ascii')
                Data_Recv = ""
            except:
                Data_Recv2 = "dummy"
                print("character error")
            break
        if Timer1.justFinished():
            print("No reply, Failed")
            break
    retries = retries + 1
    if Data_Recv2 == "AA":
        retries = 0
        break
    if retries >= 1:
        break
##DATA SENDING
for i in range(int(lens/length)+1):
    Headers = ["!","?"]
    Footers = ["!","?"]
    message = Headers[i%2] + file_bytes[i*length:(i+1)*length].decode('ascii') + Footers[i%2]
    
    retries = 0
    while True:
        status = lora.send(message, ClientAddress)
        if status is True:
            print("Packet " + str(i) + " out of " + str(int(lens/length)+1) +" packets" +" sent! (" + str((i/(int(lens/length)+1))*100) + "%", len(message))
        else:
            print("none")
        Timer1.start(3)
        Data_Recv2 = ""
        while True:
            if Data_Recv != "":
                try:
                    Data_Recv2 = Data_Recv[0:-1].decode('ascii')
                except:
                    Data_Recv2 = "dummy"
                    print("character error")
                Data_Recv = ""
                break
            if Timer1.justFinished():
                print("No reply, retrying again.")
                break
        retries = retries + 1
        if Data_Recv2 == message:
            retries = 0
            break
        if retries >= 5:
            print("Tried many times, but no reception or lossy signal")
            break 
            # return
    if retries >= 5:
        print("Tried many times, but no reception or lossy signal")
        break    

##FOOTER SENDING
retries = 0          
while True:
    status = lora.send("=", ClientAddress)
    if status is True:
        print("Footer sent!")
    else:
        print("none")
    Timer1.start(3)
    Data_Recv2 = ""
    while True:
        if Data_Recv != "":
            try:
                Data_Recv2 = Data_Recv[0:1].decode('ascii')
                Data_Recv = ""
            except:
                Data_Recv2 = "dummy"
                print("character error")
            break
        if Timer1.justFinished():
            print("No reply, Failed")
            break
    retries = retries + 1
    if Data_Recv2 == "AA":
        retries = 0
        break
    if retries >= 1:
        break
time.sleep(5)


# status = lora.send_to_wait("dhkghlkjglkhjgl", 10,retries=2)
# if status is True:
#     print("Message sent!")
# else:
#     print("No acknowledgment from recipient")

# try:
#     while True:
#         pass
# except:
#    print("some error")

# finally:
#    print("clean up")
#    lora.close()

f.close()

lora.close()
