from os import path
import os
import numpy as np

coordinates = [(301, 752), (798, 472), (303, 502), (364, 83), (664, 818), (526, 796),(799, 472),(707, 282),(318, 725),(303, 502),(363, 83),(436, 486),(502, 619),(501, 619),(690, 119),(540, 100),(608, 391),(263, 352),(426, 331),(793, 649),(661, 819),(506, 165),(607, 585)]


def toDate(filename):
    date = filename.split("-")[2]
    year = date[0:2]
    if year[0:1] == "0":
        year = int(year[1:2])
    else:
        year = int(year[0:2])
    month = date[2:4]
    if month[0:1] == "0":
        month = int(month[1:2])
    else:
        month = int(month[0:2])
    day = date[4:6]
    if day[0:1] == "0":
        day = int(day[1:2])
    else:
        day = int(day[0:2])
    return year, month, day


def toDateTime(filename):
    date = filename.split("-")[2]
    year = date[0:2]
    if year[0:1] == "0":
        year = int(year[1:2])
    else:
        year = int(year[0:2])
    month = date[2:4]
    if month[0:1] == "0":
        month = int(month[1:2])
    else:
        month = int(month[0:2])
    day = date[4:6]
    if day[0:1] == "0":
        day = int(day[1:2])
    else:
        day = int(day[0:2])
    hour = date[6:8]
    if hour[0:1] == "0":
        hour = int(hour[1:2])
    else:
        hour = int(hour[0:2])
    minute = date[8:10]
    if minute[0:1] == "0":
        minute = int(minute[1:2])
    else:
        minute = int(minute[0:2])
    return year, month, day, hour, minute


def getRadius(filename):
    year, month, day = toDate(filename)
    if before(year, month, day, 10, 6, 30):
        return 128
    else:
        return 150


def before(yearb, monthb, dayb, year, month, day):
    if yearb < year or (yearb == year and monthb < month) or (yearb == year and monthb == month and dayb < day):
        return True


def iseligable(institution, filename):
    year, month, day = toDate(filename)
    if institution == 1:
        if before(year, month, day, 18, 2, 27):
            return False
    elif institution == 2:
        if before(year, month, day, 14, 7, 31) or not before(year, month, day, 15, 3, 18):
            return False
    elif institution == 3:
        if before(year, month, day, 10, 3, 4) or not before(year, month, day, 12, 4, 12):
            return False
    elif institution == 4:
        if before(year, month, day, 12, 6, 13) or not before(year, month, day, 12, 11, 21):
            return False
    elif institution == 5:
        if before(year, month, day, 13, 9, 30) or not before(year, month, day, 14, 6, 12):
            return False
    elif institution == 6:
        if before(year, month, day, 14, 1, 23):
            return False
    elif institution == 7:
        if not before(year, month, day, 14, 8, 1) and before(year, month, day, 15, 3, 17):
            return False
    elif institution == 8:
        if not before(year, month, day, 14, 5, 7) and before(year, month, day, 14, 10, 8):
            return False
    elif institution == 9:
        if not before(year, month, day, 18, 2, 28):
            return False
    elif institution == 10:
        if not before(year, month, day, 10, 3, 5) and before(year, month, day, 12, 4, 11):
            return False
    elif institution == 11:
        if not before(year, month, day, 12, 6, 14) and before(year, month, day, 12, 11, 20):
            return False
    elif institution == 12:
        if not before(year, month, day, 14, 4, 30) and before(year, month, day, 14, 11, 12):
            return False
    elif institution == 13:
        if not before(year, month, day, 14, 7, 30):
            return False
    elif institution == 14:
        if before(year, month, day, 14, 7, 30):
            return False
    elif institution == 15:
        if before(year, month, day, 14, 1, 22):
            return False
    elif institution == 16:
        if before(year, month, day, 13, 4, 3):
            return False
    elif institution == 17:
        if not before(year, month, day, 11, 4, 12) and before(year, month, day, 12, 1, 10):
            return False
    elif institution == 18:
        if not before(year, month, day, 13, 8, 29) and before(year, month, day, 14, 3, 27):
            return False
    elif institution == 19:
        if before(year, month, day, 11, 2, 15):
            return False
    elif institution == 20:
        if before(year, month, day, 14, 1, 23):
            return False
    elif institution == 21:
        if not before(year, month, day, 13, 10, 1) and before(year, month, day, 14, 6, 11):
            return False
    elif institution == 22:
        if not before(year, month, day, 13, 4, 9) and before(year, month, day, 13, 12, 9):
            return False
    elif institution == 23:
        if not before(year, month, day, 13, 2, 15) and before(year, month, day, 13, 12, 17):
            return False
    return True


def genCounter(radius):
    counter = np.zeros(2 * radius + 1)
    radius += 1
    p = circle(radius)
    #print(p)
    for y in range(radius * 2 + 1 - 2):
        count = 0
        xp = -radius
        yp = y - radius + 1
        while (xp, yp) not in p:
            xp += 1
        while (xp, yp) in p:
            if xp == -radius:
                xp += 1
                break
            xp += 1
        while (xp, yp) not in p:
            xp += 1
            count += 1
            # print(str(xp)+", "+str(yp))
        counter[y] = count
    #print(counter)
    return counter


def decentralise(institution):
    print(1)
    counter150 = genCounter(150)
    counter128 = genCounter(128)
    files = os.listdir("D:/Drive/Institutions/Radolan/")
    progress = 0
    coord = coordinates[institution - 1]
    folder = "D:/Drive/Institutions/" + str(institution) + "/"
    if not path.isdir(folder):
        os.makedirs(folder)
    for filename in files:
        if iseligable(institution, filename):
            output = open(folder + filename, "wb")
            f = open("D:/Drive/Institutions/Radolan/" + filename, "rb")
            radius = getRadius(filename)
            lowerleft = (coord[0] - radius, coord[1] - radius)
            byte = f.read(1)
            counter = counter150
            if radius == 128:
                counter = counter128
            while int.from_bytes(byte, "big") != 3:
                byte = f.read(1)
            f.read(1)
            if lowerleft[1] > 0:
                f.read(lowerleft[1] * 900 * 2)
            for k in range((150 - radius) * 301):
                output.write(int.to_bytes(0x29C4, 2, byteorder="big"))
            for k in range(radius * 2 + 1):
                if 0 <= lowerleft[1] + k < 900:
                    extra = int((radius * 2 + 1) - counter[k])
                    f.read(lowerleft[0] * 2 + extra)
                    for j in range(extra // 2 + 150 - radius):
                        output.write(int.to_bytes(0x29C4, 2, byteorder="big"))
                    c = min(900 - lowerleft[0] - extra // 2, int(counter[k]))
                    output.write(f.read(c * 2))
                    for j in range(int(counter[k]) - c):
                        output.write(int.to_bytes(0x29C4, 2, byteorder="big"))
                    for j in range(extra // 2 + 150 - radius):
                        output.write(int.to_bytes(0x29C4, 2, byteorder="big"))
                    f.read(1800 - (lowerleft[0] * 2 + extra + 2 * c))
                else:
                    for j in range(301):
                        output.write(int.to_bytes(0x29C4, 2, byteorder="big"))
            for k in range((150 - radius) * 301):
                output.write(int.to_bytes(0x29C4, 2, byteorder="big"))
            output.close()
            progress += 1
            print("Progress: " + str((progress / len(files)) * 100) + "%")


def circle(radius):
    "Bresenham complete circle algorithm in Python"
    # init vars
    switch = 3 - (2 * radius)
    points = set()
    x = 0
    y = radius
    # first quarter/octant starts clockwise at 12 o'clock
    while x <= y:
        # first quarter first octant
        points.add((x, -y))
        # first quarter 2nd octant
        points.add((y, -x))
        # second quarter 3rd octant
        points.add((y, x))
        # second quarter 4.octant
        points.add((x, y))
        # third quarter 5.octant
        points.add((-x, y))
        # third quarter 6.octant
        points.add((-y, x))
        # fourth quarter 7.octant
        points.add((-y, -x))
        # fourth quarter 8.octant
        points.add((-x, -y))
        if switch < 0:
            switch = switch + (4 * x) + 6
        else:
            switch = switch + (4 * (x - y)) + 10
            y = y - 1
        x = x + 1
    return points

# decentralise(0)
