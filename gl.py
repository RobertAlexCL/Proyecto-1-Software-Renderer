from shaders import *
from mymath import *
from math import pi, sin, cos, tan
from obj import Obj, texture
from collections import namedtuple
from random import random



#Renderer

class Render(object):

    activeTexture = None
    light = V3(0, 0, 0)
    cameraMatrix = []
    viewMatrix = []

    def __init__(self):
        self.clear_color = color(0,0,0)
        self.draw_color = color(255,255,233)
    
    def glClear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)] 
            for y in range(self.height)
        ]
        self.zbuffer = [
            [float('inf') for x in range(self.width)]
            for y in range(self.height)
        ]

    def glCreateWindow(self, width, height): #width and height from window are renderer
        self.width = width
        self.height = height
        self.framebuffer = []
        self.glViewPort(0, 0, width, height)
        self.glClear()
    
    def point(self, x,y, color=None):
        self.framebuffer[y][x] = color or self.draw_color

    def glInit(self):
        pass

    def glViewPort(self, x, y, width, height):
        self.x_VP = x
        self.y_VP = y
        self.width_VP = width
        self.height_VP = height

        self.viewPortMatrix = [[width/2, 0, 0, x+width/2],
                                [0, height/2, 0, y+height/2],
                                [0, 0, 0.5, 0.5],
                                [0, 0, 0, 1],]
        self.createProjectionMatrix()

    def glClearColor(self, r, g, b):
        self.clear_color = color(int(round(r*255)),int(round(g*255)),int(round(b*255)))

    def glColor(self, r,g,b):
        self.draw_color = color(int(round(r*255)),int(round(g*255)),int(round(b*255)))

    def glVertex(self, x, y):
        xPixel = round((x+1)*(self.width_VP/2)+self.x_VP)
        yPixel = round((y+1)*(self.height_VP/2)+self.y_VP)
        self.point(xPixel, yPixel)
    
    def glLine(self,x1, y1, x2, y2):
        x1 = int(round((x1+1) * self.width / 2))
        y1 = int(round((y1+1) * self.height / 2))
        x2 = int(round((x2+1) * self.width / 2))
        y2 = int(round((y2+1) * self.height / 2))
        steep=abs(y2 - y1)>abs(x2 - x1)
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        if x1>x2:
            x1,x2 = x2,x1
            y1,y2 = y2,y1

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        y = y1
        offset = 0
        threshold = dx

        for x in range(x1, x2):
            if offset>=threshold:
                y += 1 if y1 < y2 else -1
                threshold += 2*dx
            if steep:
                self.framebuffer[x][y] = self.draw_color
            else:
                self.framebuffer[y][x] = self.draw_color
            offset += 2*dy

    def createProjectionMatrix(self, n = 0.1, f = 1000, fov = 60):
        t = tan((fov * pi/180)/2)*n
        r = t * self.width_VP/self.height_VP

        self.projectionMatrix = [[n/r, 0, 0, 0],
                                [0, n/t, 0, 0],
                                [0, 0, -(f+n)/(f-n), -(2*f*n)/(f-n)],
                                [0, 0, -1, 0]]

    def triangle(self, A, B, C, texcoords, normals, vertices):
        bmin, b_max = bbox(A, B, C)

        for x in range(int(bmin.x), int(b_max.x) + 1):
            if x >= self.width:
                continue
            for y in range(int(bmin.y), int(b_max.y) + 1):
                if y >= self.height:
                    continue
                u, v, w = bcenntric(A, B, C, V2(x, y))
                if w < 0 or v < 0 or u < 0:  
                    continue
                
                z = A.z * u + B.z * v + C.z * w
                
                if z < self.zbuffer[x][y] and -1 < z < 1:
                    
                    color = self.shader(self,
                    vertices = vertices, 
                    texcoords = texcoords, 
                    normals = normals, 
                    texture = self.activeTexture,
                    blendTexture = self.alternateTexture,
                    barycoords = (u, v, w))

                    self.point(x, y, color)
                    self.zbuffer[x][y] = z

    def load(self, filename, translate=V3(0, 0, 0), scale=V3(1, 1, 1), rotate = V3(0, 0, 0)):
        model = Obj(filename)
        objectMatrix = self.getObjectMatrix(translate, scale, rotate)
        rotationMatrix = self.getRotationMatrix(rotate)
        vertices = []
        texcoords = []
        normals = []

        for face in model.vfaces:
            vcount = len(face)

            if vcount == 3:
                f1 =  face[0][0] - 1
                f2 =  face[1][0] - 1
                f3 =  face[2][0] - 1

                vt1 =  face[0][1] - 1
                vt2 =  face[1][1] - 1
                vt3 =  face[2][1] - 1

                vn1 =  face[0][2] - 1
                vn2 =  face[1][2] - 1
                vn3 =  face[2][2] - 1

                vertices = [
                    trans_lineal(objectMatrix, model.vertices[f1]),
                    trans_lineal(objectMatrix, model.vertices[f2]),
                    trans_lineal(objectMatrix, model.vertices[f3]),
                ]
                texcoords = [
                    model.texcoords[vt1],
                    model.texcoords[vt2],
                    model.texcoords[vt3],
                ]
                normals = [
                    dir_trans_lineal(rotationMatrix, model.normals[vn1]),
                    dir_trans_lineal(rotationMatrix, model.normals[vn2]),
                    dir_trans_lineal(rotationMatrix, model.normals[vn3]),
                ]
                A = self.camTransfrorm(vertices[0])
                B = self.camTransfrorm(vertices[1])
                C = self.camTransfrorm(vertices[2])
                VTA, VTB, VTC = texcoords
                VNA, VNB, VNC = normals
            else:
                # assuming 4
                f1 =  face[0][0] - 1
                f2 =  face[1][0] - 1
                f3 =  face[2][0] - 1
                f4 = face[3][0] - 1

                vt1 =  face[0][1] - 1
                vt2 =  face[1][1] - 1
                vt3 =  face[2][1] - 1
                vt4 =  face[2][1] - 1

                vn1 =  face[0][2] - 1
                vn2 =  face[1][2] - 1
                vn3 =  face[2][2] - 1
                vn4 =  face[2][2] - 1

                vertices = [
                    trans_lineal(objectMatrix, model.vertices[f1]),
                    trans_lineal(objectMatrix, model.vertices[f2]),
                    trans_lineal(objectMatrix, model.vertices[f3]),
                    trans_lineal(objectMatrix, model.vertices[f4]),
                ]
                texcoords = [
                    model.texcoords[vt1],
                    model.texcoords[vt2],
                    model.texcoords[vt3],
                    model.texcoords[vt4],
                ]
                normals = [
                    dir_trans_lineal(rotationMatrix, model.normals[vn1]),
                    dir_trans_lineal(rotationMatrix, model.normals[vn2]),
                    dir_trans_lineal(rotationMatrix, model.normals[vn3]),
                    dir_trans_lineal(rotationMatrix, model.normals[vn4]),
                ]
                A = self.camTransfrorm(vertices[0])
                B = self.camTransfrorm(vertices[1])
                C = self.camTransfrorm(vertices[2])
                D = self.camTransfrorm(vertices[3])
                VTA, VTB, VTC, VTD = texcoords
                VNA, VNB, VNC, VND = normals

                self.triangle(A, C, D, (VTA, VTC, VTD), (VNA, VNC, VND), vertices)
            self.triangle(A, B, C, (VTA, VTB, VTC), (VNA, VNB, VNC), vertices)

    def glFinish(self, filename):
        f = open(filename, 'bw')

        #file header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        #image header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))   
        f.write(dword(0))
        f.write(dword(24))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0)) 
        f.write(dword(0))

        # pixel data

        for x in range(self.width):
            for y in range(self.height):
                f.write(self.framebuffer[x][y])
        
        f.close()
    
    def glFill(self, polygon):
        for y in range(self.height):
            for x in range(self.width):
                i = 0
                j = len(polygon) - 1
                inside = False
                for i in range(len(polygon)):
                    if (polygon[i][1] < y and polygon[j][1] >= y) or (polygon[j][1] < y and polygon[i][1] >= y):
                        if polygon[i][0] + (y - polygon[i][1]) / (polygon[j][1] - polygon[i][1]) * (polygon[j][0] - polygon[i][0]) < x:
                            inside = not inside
                    j = i
                if inside:
                    self.point(y,x)

    def glLookAt(self, eye, camPosition = V3(0, 0, 0)):
        forward = norm(sub(camPosition, eye))
        right = norm(cross(V3(0, 1, 0), forward))
        up = norm(cross(forward, right))
        
        self.cameraMatrix = [[right[0], up[0], forward[0], camPosition.x],
                            [right[1], up[1], forward[1], camPosition.y],
                            [right[2], up[2], forward[2], camPosition.z],
                            [0, 0, 0, 1],]
        self.viewMatrix = inv(self.cameraMatrix)

    def getRotationMatrix(self, rotate):
        pitch = rotate.x * pi/180
        yaw = rotate.y * pi/180
        roll = rotate.z * pi/180

        rotationX = [[1, 0, 0, 0],
                    [0, cos(pitch), -sin(pitch), 0],
                    [0, sin(pitch), cos(pitch), 0],
                    [0, 0, 0, 1],]

        rotationY = [[cos(yaw), 0, sin(yaw), 0],
                    [0, 1, 0, 0],
                    [-sin(yaw), 0, cos(yaw), 0],
                    [0, 0, 0, 1],]

        rotationZ = [[cos(roll), -sin(roll), 0, 0],
                    [sin(roll), cos(roll), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],]

        return matrixmul(rotationX, matrixmul(rotationY, rotationZ))

    def getObjectMatrix(self, translate = V3(0,0,0), scale = V3(1,1,1), rotate = V3(0,0,0)):
        translateMatrix = [[1, 0, 0, translate.x],
                            [0, 1, 0, translate.y],
                            [0, 0, 1, translate.z],
                            [0, 0, 0, 1],]
        scaleMatrix = [[scale.x, 0, 0, 0],
                        [0, scale.y, 0, 0],
                        [0, 0, scale.z, 0],
                        [0, 0, 0, 1],]

        rotationMatrix = self.getRotationMatrix(rotate)

        return matrixmul(translateMatrix, matrixmul(rotationMatrix, scaleMatrix))

    def camTransfrorm(self, v):
        v2 = [v[0], v[1], v[2], 1]
        v2 = trans_lineal(self.viewMatrix, v2)
        v2 = trans_lineal(self.projectionMatrix, v2)
        v2 = trans_lineal(self.viewPortMatrix, v2)
        return V3(v2[0], v2[1], v2[2])
    
    def stars(self):
        white = color(255, 255, 255)
        self.framebuffer = [
            [self.clear_color if random() > 0.01 else white  for x in range(self.width)] 
            for y in range(self.height)
        ]
        
    

r = Render()
r.activeTexture = texture('modelos/metalTexture.bmp')
r.alternateTexture = texture('modelos/rock.bmp')
r.glLookAt(V3(0, 0, -500))
r.light = V3(0, 0, -1)
r.glCreateWindow(500, 500)
r.stars()
r.shader = noise
r.load('modelos/E-TIE-B/E-TIE-B.obj', V3(200, -100, -500), V3(2, -2, 2), V3(0, 0, 0)) #desfasado
r.shader = popart
r.load('modelos/Craft/Craft.obj', V3(0, -250, -1000), V3(30, 30, 30), V3(45, 0, 0))
r.shader = blend
r.load('modelos/Mars Lander Space Capsule/Mars Lander Space Capsule.obj', V3(-250, -220, -500), V3(1, 1, 1), V3(0, 0, 0)) #desfasado
r.shader = bars
r.load('modelos/space beacon/space beacon.obj', V3(0, 250, -750), V3(0.4, 0.4, 0.4), V3(45, 0, 45))
r.shader = bary
r.load('modelos/C3PO/C3PO.obj', V3(300, -200, -500), V3(10, 10, 3), V3(0, 0, 0))
r.glFinish('out.bmp')
