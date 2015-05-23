import numpy as np
from numpy.linalg import norm, inv
from scipy.ndimage.interpolation import rotate
import math

def angle(u, v, unit='r'):
    """Returns angle between vectors u and v."""
    if all([elem == 0 for elem in u]) or all([elem == 0 for elem in v]):
        raise ValueError("Cannot pass a zero-vector")
    if len(u) != len(v):
        raise ValueError("u and v must be of the same length")
    cos = np.dot(u,v) / norm(u) / norm(v)
    rad = math.arccos(np.clip(cos, -1, 1))
    if unit == 'r':
        return rad
    elif unit == 'd':
        return math.degrees(rad)
    else:
        raise ValueError("{0} is not a valid keyword".format(output))

def midpoint(p1, p2):
    """Returns midpoint between points p1 and p2."""
    mdpt = np.divide(np.add(p1, p2), 2)
    return tuple(mdpt)

def vector(p1, p2):
    """Returns vector from p1 to p2."""
    vec = np.subtract(p2, p1)
    return tuple(vec)

def rotationMatrix(theta, unit='r'):
    """Returns rotation matrix using angle theta."""
    if unit == 'r':
        pass
    elif unit == 'd':
        theta = math.radians(theta)
    else:
        raise ValueError("{0} is not a valid keyword".format(output))
    rotmat = np.zeros((2,2))
    rotmat[0][0] = math.cos(theta)
    rotmat[0][1] = -math.sin(theta)
    rotmat[1][0] = math.sin(theta)
    rotmat[1][1] = rotmat[0][0]
    rotmat = np.matrix(rotmat)
    return rotmat

def rotate(v, theta, unit='r'):
    """Returns a rotated vector."""
    if len(v) != 2:
        raise ValueError("Dimension of v must be 2")
    if unit == 'r':
        pass
    elif unit == 'd':
        theta = math.radians(theta)
    rotmat = rotationMatrix(theta)
    v = np.matrix(v).getT()
    rotvec = (rotmat * v).getT().getA().flatten()
    return tuple(rotvec)

# Given two points that represent a leg of a right triangle and an angle,
# find the endpoint of the hypotenuse.
def endpt(p1, p2, theta, unit='r'):
    if unit == 'r':
        pass
    elif unit == 'd':
        theta = math.radians(theta)
    else:
        raise ValueError("{0} is not a valid keyword".format(output))
    mdpt = midpoint(p1, p2)
    vec = vector(p1, mdpt)
    rotvec = rotate(vec, theta)
    veclength = norm(vec) / math.cos(theta)
    rotvec = np.multiply(veclength, np.divide(rotvec, norm(rotvec)))
    return tuple(rotvec)
