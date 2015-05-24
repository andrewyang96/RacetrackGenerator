from PIL import Image, ImageDraw
from scipy.spatial import ConvexHull
from utils import endpoint, midpoint, distance, pairwise, roundrobin, getRanks
import random
import numpy as np

class TrackImage(Image.Image):
    """Representation of a racetrack circuit. Extends PIL's Image class."""
    def __init__(self, numPoints, dim, dotsBound=0.7, bgColor=(0,0,0), dotColor=(255,255,255), addedDotColor=(255,255,0), lineColor=(255,0,0), dotRadius=5, lineWidth=5, minWarpAngle=-25, maxWarpAngle=40, showDots=True, convexOnly=False):
        Image.Image.__init__(self)
        # initialize member variables
        self.mode = "RGB"
        self.points = []
        self.addedPoints = []
        self.hullVertices = []
        # initialize other member variables
        if numPoints >= 3:
            self.numPoints = numPoints
        else:
            raise ValueError("numPoints must be >= 3")
        if isinstance(dim, (list, tuple)):
            if len(dim) == 2:
                if all([isinstance(item, int) for item in dim]):
                    self.size = tuple(dim)
                else:
                    raise ValueError("Elements of dim must be integers")
            else:
                raise ValueError("dim must have exactly 2 elements")
        else:
            raise ValueError("dim must be a list or tuple")
        if dotsBound > 0 and dotsBound <= 1:
            self.dotsBound = float(dotsBound)
        else:
            raise ValueError("dotsBound must be in interval (0,1]")
        self.bgColor = bgColor
        self.dotColor = dotColor
        self.addedDotColor = addedDotColor
        self.lineColor = lineColor
        self.dotRadius = dotRadius
        self.lineWidth = lineWidth
        if minWarpAngle < maxWarpAngle:
            if minWarpAngle > -180 and minWarpAngle < 180:
                self.minWarpAngle = minWarpAngle
            else:
                raise ValueError("minWarpAngle must be within (-180,180)")
            if maxWarpAngle > -180 and maxWarpAngle < 180:
                self.maxWarpAngle = maxWarpAngle
            else:
                raise ValueError("maxWarpAngle must be within (-180,180)")
        else:
            raise ValueError("minWarpAngle cannot be smaller than maxWarpAngle")
        self.showDots = showDots
        self.convexOnly = convexOnly
        self.resetImage()
        self.generatePoints()
        self.calculateConvexHull()
        self.warp()

    def generatePoints(self):
        dotsRange = np.multiply(self.dotsBound, self.size)
        offset = np.multiply((1 - self.dotsBound) / 2, self.size)
        for i in xrange(self.numPoints):
            point = np.add(offset, np.multiply(dotsRange, (random.random(), random.random())))
            self.points.append(tuple(point))

    def calculateConvexHull(self):
        hull = ConvexHull(self.points)
        vIdx = hull.vertices
        for idx in vIdx:
            self.hullVertices.append(self.points[idx])
        # make cycle
        self.hullVertices.append(self.hullVertices[0])

    def warp(self):
        if not self.convexOnly:
            pairs = [pair for pair in pairwise(self.hullVertices)]
            for p1, p2 in pairs:
                # TODO: implement min distance check?
                mdpt = midpoint(p1, p2)
                angle = random.randint(self.minWarpAngle, self.maxWarpAngle)
                newPoint = endpoint(p1, mdpt, angle, 'd')
                self.addedPoints.append(newPoint)
            # interleave self.hullVertices and newPoints
            self.hullVertices = [point for point in roundrobin(self.hullVertices, self.addedPoints)]
    
    def resetImage(self):
        self.im = Image.core.fill("RGB", self.size, self.bgColor)

    def drawImage(self, outfile):
        self.resetImage()
        draw = ImageDraw.Draw(self)
        # draw dots
        if self.showDots:
            for point in self.points:
                upperLeft = tuple(np.subtract(point, self.dotRadius))
                lowerRight = tuple(np.add(point, self.dotRadius))
                draw.ellipse(upperLeft + lowerRight, fill=self.dotColor, outline=self.dotColor)
            for point in self.addedPoints:
                upperLeft = tuple(np.subtract(point, self.dotRadius))
                lowerRight = tuple(np.add(point, self.dotRadius))
                draw.ellipse(upperLeft + lowerRight, fill=self.addedDotColor, outline=self.addedDotColor)
        # draw lines
        draw.line(self.hullVertices, fill=self.lineColor, width=self.lineWidth)
        self.save(outfile)
