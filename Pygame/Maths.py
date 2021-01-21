from math import sqrt,hypot
from math import pi as PI
from math import e as E

#My math library containing common functions

INFINITY=float("inf")

#Clamps x to a and b
def clamp(x,a,b):
	return max(min(x,min(a,b)),max(a,b))

#Gets the distance between two points
def getDistance(a,b):
	h=hypot(b[0]-a[0],b[1]-a[1])
	for index in range(1,len(a)-1):
		h=hypot(h,b[index+1]-a[index+1])

	return h

#Returns the magnitude of a vector
def magnitude(vector):
	return getDistance(len(vector)*[0],vector)

#Normalises the vector - Keeps the direction the same but reduces the magnitude to 1
def normalise(vector):
	mag=magnitude(vector)
	return tuple(val/mag for val in vector)

#Return the dot/cross product of two vectors

def dotProduct(vector1,vector2):
	return sum(a*b for a,b in zip(vector1,vector2))

def crossProduct(vector1,vector2):
	return (vector1[1]*vector2[2]-vector1[2]*vector2[1],vector1[2]*vector2[0]-vector1[0]*vector2[2],vector1[0]*vector2[1]-vector1[1]*vector2[0])

#---List/Tuple functions---#
#They all return tuples

def addL(a,b):
	return (aval+bval for aval,bval in zip(a,b))

def subtractL(a,b):
	return (aval-bval for aval,bval in zip(a,b))

def divideL(a,b):
	return (aval/bval for aval,bval in zip(a,b))

def multiplyL(a,b):
	return (aval*bval for aval,bval in zip(a,b))