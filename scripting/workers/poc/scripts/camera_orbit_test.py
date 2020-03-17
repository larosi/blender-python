import bpy
import numpy as np
from random import randint
from math import pi

D = bpy.data
cam = D.objects['Camera']
target = D.objects['Cube'].location
print(cam.location)

cam_pos = D.objects['Camera'].location
theta, phi = np.linspace(0, 2 * np.pi, 40), np.linspace(0.25*np.pi, 0.5*np.pi, 40)
THETA, PHI = np.meshgrid(theta, phi)
R = 15
X = R * np.sin(PHI) * np.cos(THETA) + target.x
Y = R * np.sin(PHI) * np.sin(THETA) + target.y
Z = - R * np.cos(PHI)

i = randint(0,len(theta)-1)
j = randint(0,len(phi)-1)
cam.location =  (X[i][j],Y[i][j],-Z[i][j])
cam.rotation_euler = (PHI[i,j],0,pi/2+THETA[i,j])

print(cam.rotation_euler)

