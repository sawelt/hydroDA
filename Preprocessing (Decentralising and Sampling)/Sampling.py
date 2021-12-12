import FileProcessing as fp
import numpy as np
import os
import random


def sampleHighIntensityValues(file_path):
    files = os.listdir(file_path)
    d = 1
    e = 0
    random.shuffle(files)
    clusters = 0
    matrices = []
    for filename in files:
        matrices += [sampleFromFile2(file=open(file_path + filename, "rb"), c_min=20),]
    return matrices


def sampleFromFile2(file, c_min):
    c_min *= 10
    matrix = fp.processRadolanFile(file, 200)
    matrices = {}
    ind = 0
    x = np.where(matrix > c_min)
    xs = set()
    for i1 in range(len(x[0])):
        xs.add((x[0][i1], x[1][i1]))
    while xs:
        p = xs.pop()
        for j in range(32):
            for k in range(32):
                rp = (p[0] - 15 + k, p[1] - 15 + j)
                if xs.__contains__(rp):
                    xs.remove(rp)
        matrixs=np.full((32,32,1),-1)
        for l in range(32):
            for n in range(32):
                matrixs[l][n][0]=matrix[p[0]-15+l][p[1]-15+n]
        matrices[ind]=matrixs
        ind+=1
    return matrices


def sampleFromFile(file, c_min, v_max, c_size, c_tol, centralised, amount=1): # sample 32x32 rainfall events from any radolan file
    c_min *= 10
    v_max *= 10
    if centralised:
        matrix = fp.processRadolanFile(file, 200)
    else:
        matrix = fp.processDecentralisedFile(file, 100)
    matrices = {}
    points = {}
    ind = 0
    x = np.where(matrix > c_min)
    xs = set()
    count = 0
    for i1 in range(len(x[0])):
        xs.add((x[0][i1], x[1][i1]))
    while xs:
        p = xs.pop()
        x1 = p[0] - (c_size - 1) + random.randint(0, (c_size - 1))
        y1 = p[1] - (c_size - 1) + random.randint(0, (c_size - 1))
        b = False
        suma = 0
        for j in range(c_size):
            if b:
                break
            for k in range(c_size):
                val = matrix[x1 + k][y1 + j]
                if val <= 0:
                    b = True
                    break
                else:
                    suma += val
        if not b:
            if suma > (((c_size ** 2) * c_min) / c_tol):
                count += 1
                for j in range(32):
                    for k in range(32):
                        rp = (x1 - (16 - c_size // 2) + k, y1 - (16 - c_size // 2) + j)
                        if xs.__contains__(rp):
                            xs.remove(rp)
                rands = (np.random.random((amount, 4, 2)) * (16 - c_size // 2)).astype(int)
                for j in range(len(rands)):
                    ind = generate_matrix(ind, j, matrices, points, matrix, rands, v_max, x1, y1, 32 - c_size,
                                          32 - c_size, 0)
                    ind = generate_matrix(ind, j, matrices, points, matrix, rands, v_max, x1, y1, 16 - c_size // 2,
                                          32 - c_size, 1)
                    ind = generate_matrix(ind, j, matrices, points, matrix, rands, v_max, x1, y1, 32 - c_size,
                                          16 - c_size // 2, 2)
                    ind = generate_matrix(ind, j, matrices, points, matrix, rands, v_max, x1, y1, 16 - c_size // 2,
                                          16 - c_size // 2, 3)
    return matrices, points, count


def generate_matrix(ind, j, matrices, points, matrix, rands, val_max, x1, y1, z1, z2, z3):
    matrixre = np.zeros((32, 32))
    b = False
    for v1 in range(32):
        if b:
            break
        for n in range(32):
            val = matrix[x1 - z1 + n + rands[j][z3][0]][y1 - z2 + v1 + rands[j][z3][1]]
            if val == -1 or val > val_max:
                b = True
                break
            else:
                matrixre[n][v1] = val
    if not b:
        matrices[ind] = matrixre
        points[ind] = (x1 - z1 + rands[j][z3][0], y1 - z2 + rands[j][z3][1])
        ind += 1
    return ind


def sampleAndSaveGrid(start,iii,c_min, v_max, c_size, file_path, save_path, max1=200000, c_tol=2): # used to sample data for the regional disparities analysis
    files = os.listdir(file_path)
    random.shuffle(files)
    for ii in range(28-start):
        c = 0
        d = 1
        iv, iw = (ii+start)*32,iii*32
        output = open(save_path + str(iv)+","+str(iw)+" [" + str(c_min) + ", " + str(v_max) + ", " + str(
            c_tol) + ", " + str(c_size) + "]", "w")
        for filename in files:
            file = open(file_path + filename, "rb")
            byte = file.read(1)
            while int.from_bytes(byte, "big") != 3:
                byte = file.read(1)
            file.read(1)
            file.read(iv * 900 * 2)
            matrix = np.full((32, 32), -1)
            for i in range(32):
                file.read(iw * 2)
                for j in range(32):
                    byte = file.read(2)
                    intval = int.from_bytes(byte, "big")
                    if intval & 0xF000 == 0 and intval != 196:
                        matrix[i][j] = intval
                file.read(1800 - 64 - iw * 2)
            if conforms(matrix, c_min, v_max, c_size, c_tol):
                for x in range(32):
                    for y in range(32):
                        output.write(str(matrix[x][y]) + ",")
                    output.write(",")
                output.write(",")
                c += 1
            print(str(ii+start)+": "+str(d) + " files scanned. " + str(c) + " matrices selected.")
            d += 1
        output.close()


def sampleAndSaveCentralised(file_path, save_path, c_min=20, v_max=200, c_size=2, c_tol=2, ): # sample 32x32 rainfall events from a number of centralised historical events
    files = os.listdir(file_path)
    c = 0
    d = 1
    e = 0
    random.shuffle(files)
    clusters = 0
    output = open(save_path + "Radolan [" + str(c_min) + ", " + str(v_max) + ", " + str(
        c_size) + ", " + str(c_tol) + "]", "w")
    for filename in files:
        matrices, points, count = sampleFromFile(file=open(file_path + filename, "rb"), c_min=c_min,
                                                 v_max=v_max, c_tol=c_tol, centralised=True, c_size=c_size)
        e += len(matrices)
        clusters += count
        for i in matrices:
            for x in range(32):
                for y in range(32):
                    output.write(str(matrices[i][x][y]) + ",")
                output.write(",")
            output.write(filename.split("-")[2] + "," + str(points[i][0]) + "," + str(points[i][1]) + ",,,")
            c += 1
        print(str(d) + " files scanned. " + str(clusters) + " Clusters identified, " + str(e) + " matrices selected.")
        d += 1
    output.close()


def sampleAndSaveDecentralised(file_path, institution, save_path, c_min=20, v_max=200, c_size=2, c_tol=2): # sample 32x32 rainfall events from a number of decentralised historical events
    files = os.listdir(file_path)
    c = 0
    d = 1
    e = 0
    random.shuffle(files)
    clusters = 0
    output = open(save_path + "I"+str(institution)
                  + " [" + str(c_min) + ", " + str(v_max) + ", " + str(
        c_size) + ", " + str(c_tol) + "]", "w")
    for filename in files:
        matrices, points, count = sampleFromFile(file=open(file_path + filename, "rb"), c_min=c_min,
                                                 v_max=v_max, c_tol=c_tol, centralised=False, c_size=c_size)
        e += len(matrices)
        clusters += count
        for i in matrices:
            for x in range(32):
                for y in range(32):
                    output.write(str(matrices[i][x][y]) + ",")
                output.write(",")
            output.write(filename.split("-")[2] + "," + str(points[i][0]) + "," + str(points[i][1]) + ",,,")
            c += 1
        print(str(d) + " files scanned. " + str(clusters) + " Clusters identified, " + str(e) + " matrices selected.")
        d += 1
    output.close()


def conforms(matrix, cluster_min, val_max, c_size, cluster_tolerance=2): # check if cluster conditions apply for 32x32 event
    cluster_min *= 10
    val_max *= 10
    x = np.where(matrix > cluster_min)
    if np.amax(matrix) > val_max or np.amin(matrix) == -1:
        return False
    xs = set()
    for i1 in range(len(x[0])):
        xs.add((x[0][i1], x[1][i1]))
    while xs:
        p = xs.pop()
        x1 = p[0] - c_size // 2
        y1 = p[1] - c_size // 2
        suma = 0
        b=False
        if 0 <= x1 <= 32 - c_size and 0 <= y1 <= 32 - c_size:
            for j in range(c_size):
                for k in range(c_size):
                    val = matrix[x1 + k][y1 + j]
                    if val == 0:
                        b=True
                        break
                    suma += val
                if b:
                    break
            if suma > (((c_size ** 2) * cluster_min) / cluster_tolerance) and not b:
                return True
    return False


if __name__ == "__main__":
    sampleAndSaveCentralised("D:/Drive/Institutions/Radolan/", "Institutions/Radolan/", 20, 200, 2, 2)