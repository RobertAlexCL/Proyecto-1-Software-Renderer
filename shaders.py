
from random import random
from mymath import color
from mymath import *

def flat(renderer, **kwargs):
    text = kwargs['texture']
    VA, VB, VC = kwargs['vertices']
    VTA, VTB, VTC = kwargs['texcoords']
    u, v, w = kwargs['barycoords']
    lx, ly, lz = renderer.light
    light = V3(lx*-1, ly*-1, lz*-1)

    tx = VTA[0]*u + VTB[0]*v + VTC[0]*w
    ty = VTA[1]*u + VTB[1]*v + VTC[1]*w
    r, g, b = text.getColor(tx, ty)

    normal = cross(sub(VB, VA), sub(VC, VA))
    normal = norm(normal)
    intensity = dot(normal, light)

    if intensity > 1:
        intensity = 1
    if intensity < 0:
        intensity = 0

    r *= intensity
    g *= intensity
    b *= intensity

    return color(r*255, g*255, b*255)


def phong(renderer, **kwargs):
    text = kwargs['texture']
    VTA, VTB, VTC = kwargs['texcoords']
    VNA, VNB, VNC = kwargs['normals']
    u, v, w = kwargs['barycoords']
    lx, ly, lz = renderer.light
    light = V3(lx*-1, ly*-1, lz*-1)

    normal = V3(VNA[0] * u + VNB[0] * v + VNC[0] * w,
                VNA[1] * u + VNB[1] * v + VNC[1] * w,
                VNA[2] * u + VNB[2] * v + VNC[2] * w)
    
    intensity = dot(normal, light)

    tx = VTA[0]*u + VTB[0]*v + VTC[0]*w
    ty = VTA[1]*u + VTB[1]*v + VTC[1]*w
    r, g, b = text.getColor(tx, ty)

    if intensity > 1:
        intensity = 1
    if intensity < 0:
        intensity = 0

    r *= intensity
    g *= intensity
    b *= intensity

    return color(r*255, g*255, b*255)


def gourad(renderer, **kwargs):
    text = kwargs['texture']
    VTA, VTB, VTC = kwargs['texcoords']
    VNA, VNB, VNC = kwargs['normals']
    u, v, w = kwargs['barycoords']
    lx, ly, lz = renderer.light
    light = V3(lx*-1, ly*-1, lz*-1)

    intensityA = dot(VNA, light)
    intensityB = dot(VNB, light)
    intensityC = dot(VNC, light)
    
    intensity = intensityA*u + intensityB*v + intensityC*w

    tx = VTA[0]*u + VTB[0]*v + VTC[0]*w
    ty = VTA[1]*u + VTB[1]*v + VTC[1]*w
    r, g, b = text.getColor(tx, ty)

    if intensity > 1:
        intensity = 1
    if intensity < 0:
        intensity = 0

    r *= intensity
    g *= intensity
    b *= intensity

    return color(r*255, g*255, b*255)

def noise(renderer, **kwargs):
    VNA, VNB, VNC = kwargs['normals']
    u, v, w = kwargs['barycoords']
    lx, ly, lz = renderer.light
    light = V3(lx*-1, ly*-1, lz*-1)

    normal = V3(VNA[0] * u + VNB[0] * v + VNC[0] * w,
                VNA[1] * u + VNB[1] * v + VNC[1] * w,
                VNA[2] * u + VNB[2] * v + VNC[2] * w)
    
    normal = norm(normal)
    intensity = dot(normal, light)

    r = g = b = random()

    if intensity > 1:
        intensity = 1
    if intensity < 0:
        intensity = 0

    r *= intensity
    g *= intensity
    b *= intensity

    return color(r*255, g*255, b*255)


def toon(renderer, **kwargs):
    text = kwargs['texture']
    VNA, VNB, VNC = kwargs['normals']
    VTA, VTB, VTC = kwargs['texcoords']
    u, v, w = kwargs['barycoords']
    lx, ly, lz = renderer.light
    light = V3(lx*-1, ly*-1, lz*-1)

    tx = VTA[0]*u + VTB[0]*v + VTC[0]*w
    ty = VTA[1]*u + VTB[1]*v + VTC[1]*w
    r, g, b = text.getColor(tx, ty)

    normal = V3(VNA[0] * u + VNB[0] * v + VNC[0] * w,
                VNA[1] * u + VNB[1] * v + VNC[1] * w,
                VNA[2] * u + VNB[2] * v + VNC[2] * w)
    intensity = dot(normal, light)

    if intensity > 1:
        intensity = 1
    elif intensity < 0.25:
        intensity = 0
    elif intensity < 0.5:
        intensity = 0.25
    elif intensity < 0.75:
        intensity = 0.5
    else:
        intensity = 1

    r *= intensity
    g *= intensity
    b *= intensity

    return color(r*255, g*255, b*255)


def popart(renderer, **kwargs):
    text = kwargs['texture']
    VNA, VNB, VNC = kwargs['normals']
    VTA, VTB, VTC = kwargs['texcoords']
    u, v, w = kwargs['barycoords']
    lx, ly, lz = renderer.light
    light = V3(lx*-1, ly*-1, lz*-1)

    tx = VTA[0]*u + VTB[0]*v + VTC[0]*w
    ty = VTA[1]*u + VTB[1]*v + VTC[1]*w
    r, g, b = text.getColor(tx, ty)

    normal = V3(VNA[0] * u + VNB[0] * v + VNC[0] * w,
                VNA[1] * u + VNB[1] * v + VNC[1] * w,
                VNA[2] * u + VNB[2] * v + VNC[2] * w)
    normal = norm(normal)
    intensity = dot(normal, light)

    if intensity > 1:
        intensity = 1
    elif intensity < 0.5:
        intensity = 0
    else:
        intensity = 1

    r = g*(1-intensity*2) + r*intensity*2
    g = b*(1-intensity*2) + g*intensity*2
    b = r*(1-intensity*2) + b*intensity*2

    if r > 1:
        r = 1
    if r < 0:
        r = 0
    if g > 1:
        g = 1
    if g < 0:
        g = 0
    if b > 1:
        b = 1
    if b < 0:
        b = 0

    return color(r*255, g*255, b*255)

def bars(renderer, **kwargs):
    VTA, VTB, VTC = kwargs['texcoords']
    VNA, VNB, VNC = kwargs['normals']
    u, v, w = kwargs['barycoords']
    lx, ly, lz = renderer.light
    light = V3(lx*-1, ly*-1, lz*-1)

    normal = V3(VNA[0] * u + VNB[0] * v + VNC[0] * w,
                VNA[1] * u + VNB[1] * v + VNC[1] * w,
                VNA[2] * u + VNB[2] * v + VNC[2] * w)
    
    normal = norm(normal)
    intensity = dot(normal, light)

    tx = VTA[0]*u + VTB[0]*v + VTC[0]*w
    ty = VTA[1]*u + VTB[1]*v + VTC[1]*w
    r = 1
    g = 0.54
    b = 0
    if int(tx*ty*10000)%2 == 0:
        r = g = 0
        b = 1

    if intensity > 1:
        intensity = 1
    if intensity < 0:
        intensity = 0

    r *= intensity
    g *= intensity
    b *= intensity

    return color(r*255, g*255, b*255)


def bary(renderer, **kwargs):
    VNA, VNB, VNC = kwargs['normals']
    u, v, w = kwargs['barycoords']
    lx, ly, lz = renderer.light
    light = V3(lx*-1, ly*-1, lz*-1)
    r = u
    g = v
    b = w

    normal = V3(VNA[0] * u + VNB[0] * v + VNC[0] * w,
                VNA[1] * u + VNB[1] * v + VNC[1] * w,
                VNA[2] * u + VNB[2] * v + VNC[2] * w)
    
    normal = norm(normal)
    intensity = dot(normal, light)
    

    if intensity > 1:
        intensity = 1
    if intensity < 0:
        intensity = 0

    r *= intensity
    g *= intensity
    b *= intensity

    return color(r*255, g*255, b*255)


def blend(renderer, **kwargs):
    text = kwargs['texture']
    text2 = kwargs['blendTexture']
    VTA, VTB, VTC = kwargs['texcoords']
    VNA, VNB, VNC = kwargs['normals']
    u, v, w = kwargs['barycoords']
    lx, ly, lz = renderer.light
    light = V3(lx*-1, ly*-1, lz*-1)

    blend_dir = V3(0, -1, 0)

    normal = V3(VNA[0] * u + VNB[0] * v + VNC[0] * w,
                VNA[1] * u + VNB[1] * v + VNC[1] * w,
                VNA[2] * u + VNB[2] * v + VNC[2] * w)
    
    normal = norm(normal)
    intensity = dot(normal, light)
    blend = dot(normal, blend_dir)

    tx = VTA[0]*u + VTB[0]*v + VTC[0]*w
    ty = VTA[1]*u + VTB[1]*v + VTC[1]*w
    r, g, b = text.getColor(tx, ty)
    r2, g2, b2 = text2.getColor(tx, ty)

    if blend > 1:
        blend = 1
    if blend < 0:
        blend = 0

    r = r*blend + r2*(1-blend)
    g = g*blend + g2*(1-blend)
    b = b*blend + b2*(1-blend)


    if intensity > 1:
        intensity = 1
    if intensity < 0:
        intensity = 0

    r *= intensity
    g *= intensity
    b *= intensity

    return color(r*255, g*255, b*255)