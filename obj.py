from os import error
import struct
from mymath import *

def try_int(s, base=10, val=None):
  try:
    return int(s, base)
  except ValueError:
    return val

class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()

        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.vfaces = []
        self.read()

    def read(self):
        for line in self.lines:
            if line:
                if not(line[0] in 'vf'):
                    continue
                prefix, value = line.split(' ', 1)
                try:
                    if prefix == 'v':
                        self.vertices.append(list(map(float, value.split(' '))))
                    elif prefix == 'vt':
                        self.texcoords.append(list(map(float, value.split(' '))))
                    elif prefix == 'vn': 
                        self.normals.append(list(map(float, value.split(' '))))
                    elif prefix == 'f':
                        #l = [face for face in value.split(' ') if len(face) > 1]
                        #print(l)
                        self.vfaces.append([list(map(int , face.split('/'))) for face in value.split(' ') if len(face) > 1])
                except:
                    print(len(self.vertices))
                    print(len(self.texcoords))
                    print(len(self.normals))
                    print(len(self.vfaces))
                    #print(error)
                    raise Exception('parse err')



class texture(object):

    def __init__(self, filename):
        self.filename = filename
        with open(self.filename, "rb") as image:
            image.seek(10)
            headerSize = struct.unpack('=l', image.read(4))[0]

            image.seek(14 + 4)
            self.width = struct.unpack('=l', image.read(4))[0]
            self.height = struct.unpack('=l', image.read(4))[0]

            image.seek(headerSize)

            self.pixels = []

            for y in range(self.height):
                self.pixels.append([])
                for x in range(self.width):
                    b = ord(image.read(1)) / 255
                    g = ord(image.read(1)) / 255
                    r = ord(image.read(1)) / 255

                    self.pixels[y].append((r,g,b))
    
    def getColor(self, tx, ty):
        if 0<=tx<1 and 0<=ty<1:
            x = int(tx * self.width)
            y = int(ty * self.height)
            return self.pixels[y][x]
        else:
            return color(0,0,0)