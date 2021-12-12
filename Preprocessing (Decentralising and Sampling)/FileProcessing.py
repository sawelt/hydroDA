import numpy as np
import os


def processRadolanFile(file, additional=200):
    matrix = np.full((900 + additional, 900 + additional), -1)
    byte = file.read(1)
    while int.from_bytes(byte, "big") != 3:
        byte = file.read(1)
    file.read(1)
    for x in range(900):
        for y in range(900):
            byte = file.read(2)
            intval = int.from_bytes(byte, "big")
            if intval & 0xF000 == 0 and intval != 196:
                matrix[x + int(additional / 2)][y] = intval
    return matrix


def processDecentralisedFile(file, additional=100):
    matrix = np.full((301 + additional, 301 + additional), -1)
    for x in range(301):
        for y in range(301):
            byte = file.read(2)
            intval = int.from_bytes(byte, "big")
            if intval & 0xF000 == 0 and intval != 196:
                matrix[x + int(additional / 2)][y + int(additional / 2)] = intval
    return matrix
