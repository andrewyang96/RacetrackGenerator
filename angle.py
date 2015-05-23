import numpy as np
from numpy.linalg import norm

def angle(u, v, output='r'):
    if all([elem == 0 for elem in u]) or all([elem == 0 for elem in v]):
        raise ValueError("Cannot pass a zero-vector")
    if len(u) != len(v):
        raise ValueError("u and v must be of the same length")
    cos = np.dot(u,v) / norm(u) / norm(v)
    rad = np.arccos(np.clip(cos, -1, 1))
    if output == 'r':
        return rad
    elif output == 'd':
        return np.degrees(rad)
    else:
        raise ValueError("{0} is not a valid keyword".format(output))
