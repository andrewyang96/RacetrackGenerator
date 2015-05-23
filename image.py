from PIL import Image, ImageDraw
from scipy.spatial import ConvexHull
from utils import endpt, mdpt
import random
import numpy as np

class TrackImage(Image.Image):
    """Representation of a racetrack circuit. Extends PIL's Image class."""
    def __init__(self, numPoints, dim, dotsBound=0.75, bgColor=(0,0,0), dotColor=(255,255,255), lineColor=(255,0,0), dotRadius=5, lineWidth=5, showDots=True):
        Image.Image.__init__(self)
        # initialize member variables
        self.mode = "RGB"
        self.points = []
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
        self.lineColor = lineColor
        self.dotRadius = dotRadius
        self.lineWidth = lineWidth
        self.showDots = showDots
        self.resetImage()
        self.generatePoints()
        self.calculateConvexHull()

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
        # draw lines
        draw.line(self.hullVertices, fill=self.lineColor, width=self.lineWidth)
        self.save(outfile)
