import base64
f = open("/home/pi/Desktop/Main/GUI/Video.jpg", "rb+")
x = f.read()
x = base64.b64encode(x)

print(x[0:500])
lens = len(x)
print(lens/250)
for i in range(int(lens/250)+1):
    print(x[i*250:(i+1)*250])
    if i == 2:
        break
f.close()
