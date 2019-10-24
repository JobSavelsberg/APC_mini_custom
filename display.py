import APC_mini_custom as APC
O = 0
G = 1
g = 2
R = 3
r = 4
Y = 5
y = 6

CLEAR = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
RED = [
    [R, R, R, R, R, R, R, R],
    [R, R, R, R, R, R, R, R],
    [R, R, R, R, R, R, R, R],
    [R, R, R, R, R, R, R, R],
    [R, R, R, R, R, R, R, R],
    [R, R, R, R, R, R, R, R],
    [R, R, R, R, R, R, R, R],
    [R, R, R, R, R, R, R, R]
]
JOB = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, G, Y, Y, R, 0, 0],
    [0, 0, G, Y, Y, R, 0, 0],
    [0, 0, G, Y, Y, R, R, R],
    [G, 0, G, Y, Y, R, 0, R],
    [G, G, G, Y, Y, R, R, R],
    [G, G, G, Y, Y, R, R, R],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

def clearAll (apc):
    clearM(apc)
    clearV(apc)
    clearH(apc)

def clearM (apc):
    img(apc, CLEAR)

def clearV (apc):
    allV(apc, 0)

def clearH (apc):
    allH(apc, 0)

def img (apc, img):
    for y in range(8):
        for x in range(8):
            apc._send_midi((APC.NOTE_ON_STATUS, x+(7-y)*8 , img[y][x]))

def M (apc, x, y, color):
    M(apc, x + y * 8, color)
def M (apc, i, color):
    apc._send_midi((APC.NOTE_ON_STATUS, i, color))

def V(apc, i, color):
    apc._send_midi((APC.NOTE_ON_STATUS, 82+i, color))

def H(apc, i, color):
    apc._send_midi((APC.NOTE_ON_STATUS, 64+i, color))

def allV(apc, color):
    for v in range(8):
        V(apc, v, color)
def allH(apc, color):
    for h in range(8):
        H(apc, h, color)