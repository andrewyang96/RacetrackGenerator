# Source: http://en.wikipedia.org/wiki/Centripetal_Catmull%E2%80%93Rom_spline
# http://people.wku.edu/qi.li/teaching/446/cg14_curve_surface.pdf
import numpy as np
from utils import distance

def CatmullRomSpline(P0, P1, P2, P3, nPoints=100):
    """
    P0, P1, P2, and P3 should be (x,y) point pairs that define the Catmull-Rom spline.
    nPoints is the number of points to include in this curve segment.
    """
    # Convert the points to numpy so that we can do array multiplication
    P0, P1, P2, P3 = map(np.array, [P0, P1, P2, P3])

    # Calculate t0 to t4
    alpha = 0.5
    def tj(ti, Pi, Pj):
        xi, yi = Pi
        xj, yj = Pj
        return ( ( (xj-xi)**2 + (yj-yi)**2 )**0.5 )**alpha + ti

    t0 = P0[0]
    t1 = tj(t0, P0, P1)
    t2 = tj(t1, P1, P2)
    t3 = P3[0]

    # Only calculate points between P1 and P2
    t = np.linspace(t1,t2,nPoints)

    # Reshape so that we can multiply by the points P0 to P3
    # and get a point for each value of t.
    t = t.reshape(len(t),1)

    A1 = (t1-t)/(t1-t0)*P0 + (t-t0)/(t1-t0)*P1
    A2 = (t2-t)/(t2-t1)*P1 + (t-t1)/(t2-t1)*P2
    A3 = (t3-t)/(t3-t2)*P2 + (t-t2)/(t3-t2)*P3

    B1 = (t2-t)/(t2-t0)*A1 + (t-t0)/(t2-t0)*A2
    B2 = (t3-t)/(t3-t1)*A2 + (t-t1)/(t3-t1)*A3

    C  = (t2-t)/(t2-t1)*B1 + (t-t1)/(t2-t1)*B2
    return C

def CatmullRomLoop(loop, pointsPerUnitDist=1.):
    """
    Calculate Catmull Rom for a list of points, named loop, with loop[0] == loop[-1].
    """
    if len(loop) < 4:
        raise ValueError("Loop must have at least 4 points in it")
    ret = []
    # Add extra control points to ends
    loop = [loop[-2],] + loop + [loop[1],]
    # Produce coords for loop
    for i in xrange(len(loop)-3):
        numPoints = int(distance(loop[i+1], loop[i+2]) * pointsPerUnitDist)
        ret.append(CatmullRomSpline(loop[i], loop[i+1], loop[i+2], loop[i+3], nPoints=numPoints))
    ret = [tuple(coords) for seg in ret for coords in seg]
    return ret
