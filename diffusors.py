import numpy as np
import bpy
import bmesh
import mathutils

modulo = 13
frequencyStart = 1000
soundSpeed = 343.6

scene = bpy.context.scene

# deleting all objects in the scene
def deleteAllObjectsFromScene():
    candidateList = [item.name for item in bpy.data.objects if item.type == "MESS"]

    for objectName in candidateList:
        bpy.data.objects[objectName].select = True
    bpy.ops.object.delete()

    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)

def xySquare2d(z, scale=1.0):
    r = [-scale, scale]
    return [mathutils.Vector((x, y, z)) for x in r for y in r]

def createCube(height, side):
    mesh = bpy.data.meshes.new("mesh")
    points = list()
    points.extend(xySquare2d(z=0, scale=side))
    points.extend(xySquare2d(z=height, scale=side))
    bottomFace = [(0, 1, 3, 2)]
    topFace = [(4, 5, 7, 6)]
    outerFaces = [(0, 1, 5, 4), (0, 2, 6, 4), (2, 3, 7, 6), (1, 3, 7, 5)]
    faces = bottomFace + topFace + outerFaces
    mesh.from_pydata(points, [], faces)
    obj = bpy.data.objects.new("obj", mesh)
    return obj

def moveObject(obj, x, y):
    obj.location = mathutils.Vector((x, y, 0))
    return obj

def addObject(obj):
    scene.collection.objects.link(obj)

def createPattern(numberOfElements):
    XX = np.zeros((numberOfElements, numberOfElements));
    for x in range(numberOfElements):
        row = ""
        for y in range(numberOfElements):
            alpha = x + 1
            beta = y + 1
            XX[x, y] = (alpha**2 + beta**2) % modulo * soundSpeed / frequencyStart / 2 / modulo
            row += str(XX[x, y]) + ", "
        print(row)
    return XX


def createDiffusor(sideSize, numOfElements):
    width = sideSize / numOfElements
    pattern = createPattern(numOfElements)
    maximum = np.max(pattern)
    pattern = np.abs(pattern - maximum)
    for x in range(pattern.shape[0]):
        for y in range(pattern.shape[1]):
            cube = createCube(pattern[x, y], width/2)
            cube = moveObject(cube, (x-numOfElements/2)*width, (y-numOfElements/2)*width)
            addObject(cube)


deleteAllObjectsFromScene()
createDiffusor(0.6, 12)