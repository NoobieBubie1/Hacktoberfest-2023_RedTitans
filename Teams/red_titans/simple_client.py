import socket
import random
from PIL import Image

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.201.77.56", 4321))

def pixel(x,y,r,g,b,a=255):
    if a == 255:
        s.send(f"PX {x} {y} {r:02x}{g:02x}{b:02x}\n".encode("utf-8"))
    else:
        s.send(f"PX {x} {y} {r:02x}{g:02x}{b:02x}{a:02x}\n".encode("utf-8"))

def line(x1,y1,x2,y2,r,g,b):
    x,y = x1,y1
    dx = abs(x2 - x1)
    dy = abs(y2 -y1)
    
    if dx == 0:
        rect(x1,y1,dy,1,r,g,b)
        return
    if dy == 0:
        rect(x1,y1,1,dx,r,g,b)
        return
    
    gradient = dy/float(dx)

    if gradient > 1:
        dx, dy = dy, dx
        x, y = y, x
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    p = 2*dy - dx    

    for k in range(2, dx + 2):
        if p > 0:
            y = y + 1 if y < y2 else y - 1
            p = p + 2 * (dy - dx)
        else:
            p = p + 2 * dy

        x = x + 1 if x < x2 else x - 1

        pixel(x,y,r,g,b)

def rect(x,y,w,h,r,g,b):
  for i in range(x,x+w):
    for j in range(y,y+h):
      pixel(i,j,r,g,b)

def worm(x,y,n,r,g,b):
    while n:
        rx = random.randint(0,200)-100
        ry = random.randint(0,200)-100
        line(x, y, x + rx, y + ry, r, g, b)
        x += rx
        y += ry
        n -= 1

def blit(x, y, image):
    for ix in range(0, image.width):
        for iy in range(0, image.height):
            r, g, b = image.getpixel((ix,iy))
            pixel(ix,iy,r,g,b)

glasses = Image.open('thug.png')
glasses = glasses.resize((300,75))

for y in range(0, 50):
    img = Image.open('cat.jpg')
    smallimg = img.resize((638,358))
    smallimg.paste(glasses, (300,y), glasses)
    blit(1000, 0, smallimg)



s.close()