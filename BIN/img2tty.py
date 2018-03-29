#!/usr/bin/env python3
from PIL import Image
from colr import rgb2term, color
from sys import argv

def printPixel(r, g, b, a, width=2):
    if a:
        print(color(' ' * width, back=rgb2term(r, g, b)), end='')
    else:
        print(' ' * width, end='')

def resize(img, maxWidth=48):
    if img.size[0] > maxWidth:
        factor = img.size[0] // maxWidth + 1
        return img.resize((img.size[0] // factor,
                img.size[1] // factor),
                Image.ANTIALIAS)
    return img


img = resize(Image.open(argv[1]).convert('RGBA'))
pixmap = img.load()
for x in range(img.size[1]):
    for y in range(img.size[0]):
        pixel = pixmap[y,x]
        printPixel(pixel[0], pixel[1], pixel[2], pixel[-1] > 128)
    print()
