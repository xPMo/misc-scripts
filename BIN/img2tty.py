#!/usr/bin/env python3
from PIL import Image
from colr import rgb2term, color
from sys import argv
from time import sleep

def printPixel(r, g, b, a, w):
    if a:
        print(color(' ' * w, back=rgb2term(r, g, b)), end='')
    else:
        print(' ' * w, end='')

# simple resize
def resize(img, maxWidth):
    if img.size[0] > maxWidth:
        factor = img.size[0] // maxWidth + 1
        return img.resize((img.size[0] // factor,
                img.size[1] // factor),
                Image.NEAREST)
    return img

def printImage(img, maxWidth=48, pixelWidth=2):
    img = resize(img, maxWidth)
    pixmap = img.load()
    for x in range(img.size[1]):
        for y in range(img.size[0]):
            pixel = pixmap[y,x]
            printPixel(pixel[0], pixel[1], pixel[2], pixel[-1] > 128, pixelWidth)
        print()

img = Image.open(argv[1]).convert('RGBA')
try:
    w=int(argv[2])
except:
    w = 48
try:
    p = int(argv[3])
except:
    p = 2
printImage(img, w, p)
