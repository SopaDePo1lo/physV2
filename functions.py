import math
import objects as phys

def crossProductVector(vector1, vector2):
    return vector1.x*vector2.y - vector1.y*vector2*x

def crossProductVectorScalar(vector, scalar):
    return phys.Vector(scalar*vector.y, -scalar*vector.x)

def crossProductScalarVector(scalar, vector):
    return phys.Vector(-scalar*vector.y, scalar*vector.x)

def addSpring(pi, i, j, spring_arr, arr):
    spring_arr[pi].indexes = (i, j)
    spring_arr[pi].length = math.sqrt(((arr[i].position.x - arr[j].position.x)**2) + ((arr[i].position.y - arr[j].position.y)**2))
    return spring_arr
