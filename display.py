import APC_mini_custom as APC
O = 0
G = 1
g = 2
R = 3
r = 4
Y = 5
y = 6

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

def clear (apc):
    apc._update_hardware()

def img (apc, img):
    for y in range(8):
        for x in range(8):
            apc.really_do_send_midi((APC.NOTE_ON_STATUS, x+(7-y)*8 , img[y][x]))

def on (apc, x, y, color):
    apc.really_do_send_midi((APC.NOTE_ON_STATUS, x+y*8, color))

def off (apc, x, y):
    apc.really_do_send_midi((APC.NOTE_ON_STATUS, x+y*8, 0))