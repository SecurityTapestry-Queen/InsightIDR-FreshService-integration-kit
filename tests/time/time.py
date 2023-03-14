from datetime import datetime

def timeCheck():
    now = datetime.now()
    formatted = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    # print(formatted)

    lasttime = open("lasttime.txt", "r")
    lasttimedata = lasttime.read()
    lasttime.close()
    print("Last Check: " + lasttimedata)

    t1 = datetime.strptime(formatted, "%Y-%m-%dT%H:%M:%S.%fZ")
    # print(t1)

    t2 = datetime.strptime(lasttimedata, "%Y-%m-%dT%H:%M:%S.%fZ")
    # print(t2)

    if t1 > t2:
        print("old data")
        updateLastTime()
    else:
        print("no update")

def updateLastTime():
    lasttime = open("lasttime.txt", "w")
    write = lasttime.write(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
    lasttime.close()
    print('updated')

timeCheck()