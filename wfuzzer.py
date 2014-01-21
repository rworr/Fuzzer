# Python script to generate random valid programs for a given language

import random

ws = [" ", "\t", "\n"]
encodeA = 65
encodeZ = 90
encodea = 97
encodez = 122

def whitespace():
    chars = random.randint(0,5)
    for i in range(0,chars):
        num = random.randint(0,2)
        wavefile.write(ws[num])

def bits():
    num = random.randint(1,100)
    iter = 0
    while(iter < num):
        whitespace()
        wavefile.write(str(random.randint(0,1)))
        whitespace()
        iter = iter + 1

def digit():
    wavefile.write(str(random.randint(0,9)))

def char():
    if random.randint(0,1) == 1:
        wavefile.write(chr(random.randint(encodeA, encodeZ)))
    else:
        wavefile.write(chr(random.randint(encodea, encodez)))

def id():
    char()
    num = random.randint(0,100)
    for i in range(0,num):
        r = random.randint(0,2)
        if r == 0:
            char()
        elif r == 1:
            digit()
        else:
            wavefile.write("_")

def waveform():
    whitespace()
    id()
    whitespace()
    wavefile.write(":")
    bits()
    wavefile.write(";")
    whitespace();

def wprogram():
    global wavefile
    wavefile = open("wave" + str(filenum) + ".wave", 'w')
    num = random.randint(1,100)
    iter = 0
    while(iter < num):
        waveform();
        wavefile.write("\n")
        iter = iter + 1

random.seed();
filenum = 0
num = random.randint(1,100)
while(filenum < num):
    wprogram();
    filenum = filenum + 1
