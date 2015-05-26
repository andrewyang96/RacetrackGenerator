from image import TrackImage
import catmullrom

if __name__ == "__main__":
    img = TrackImage(50, (2000,2000), dotRadius=20, lineWidth=40, showDots=False)
    img.drawImage("test.png")
