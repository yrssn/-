import time

time1 = int(time.time())
time2 = 3
# print(time1+time2)
print(time1)
# print(time1+time2)
while True:
    if int(time.time())-(time1+time2)==0:
        print(int(time.time()))
        print(11111)
        break


