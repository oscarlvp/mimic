import argparse
import cv2
import numpy as np

def lemniscate(width, height, foci, radius):
    '''
    Renders a lemniscate with given foci 
    and radius in an image of the given size.
    The value for the radius should be a number in [0, 1].
    Instead of comparing the raz distance, the distance matrix is first
    normalized and then compared agains the radius.

    @param width: Width of the resulting image
    @param height: height of the resulting image
    @param foci: Foci of the lemniscate to render
    @param radius: A number in [0,1] controlling the threshold 
    '''
    #TODO: Improve the radius traeatment
    if not len(foci):
        return np.zeros((height, width))
    acc = np.ones((height, width))
    x = np.arange(width)
    y = np.arange(height)
    for xp, yp in foci:
        X, Y = np.meshgrid((x - xp)**2, (y - yp)**2)
        np.multiply(X + Y, acc, out=acc)
    cv2.normalize(acc, acc, norm_type=cv2.NORM_MINMAX)
    cv2.threshold(acc, radius, 1, cv2.THRESH_BINARY, acc)
    return 1 - acc


class LemniscateApp:

    def __init__(self, title='lemniscate', width=640, height=480, radius=5):
        self.title = title
        self.width = width
        self.height = height
        self.track = min(radius, 100)
        
        self.clear()
        self.setup()

    def run(self):
        while True:
            key = cv2.waitKey(30)
            if key == ord('r'):
                self.remove_last_focus()
            elif key == ord('c'):
                self.clear()
            elif key == ord('s'):
                self.save()
            elif key == 27:
                cv2.destroyWindow(self.title)
                break
            cv2.imshow(self.title, self.lemniscate)
    
    def setup(self):
        cv2.namedWindow(self.title)
        cv2.setMouseCallback(self.title, self.mouse_callback)
        cv2.createTrackbar('Radius', self.title, self.track, 100, self.radius_changed)


    def mouse_callback(self, evt, x, y, flags, params):
        if evt == cv2.EVENT_LBUTTONDOWN:
            self.add_focus(x, y)
    
    def radius_changed(self, track):
        self.track = track
        self.render()

    def track_to_radius(self):
        return self.track * .1 / 100;

    def add_focus(self, x, y):
        self.foci.append((x, y))
        self.render()

    def remove_last_focus(self):
        if not len(self.foci):
            return
        self.foci.pop()
        self.render()

    def clear(self):
        self.foci = []
        self.lemniscate = np.zeros((self.height, self.width))
    
    def save(self):
        filename = self.title + '.jpg'
        cv2.imwrite(filename, 255*self.lemniscate)
        print('Image save to ' + filename)

    def render(self):
        self.lemniscate =  lemniscate(self.width, self.height, self.foci, self.track_to_radius())
    
def main():
    parser = argparse.ArgumentParser(
        description="Interactive lemniscate drawing. Mouse click sets a focus. Pressing 'r' removes the last added focus. 'c' will erase all foci. 's' will save the image to disk.")
    parser.add_argument(
        '--title', '-t', 
        dest='title', default='lemniscate',
        help='Title of the window and the image to save')
    parser.add_argument(
        '--width', '-w', 
        dest='width', type=int, default=640,
        help='Width of the image')
    parser.add_argument(
        '--height', '-e', 
        dest='height', type=int, default=480,
        help='Height of the image')
    parser.add_argument(
        '--radius', '-r', 
        dest='radius', type=int, default=5,
        help='Value of the radius. Must be between 0 and 100')
    arguments = parser.parse_args()

    print(parser.description)
    app = LemniscateApp(arguments.title, arguments.width, arguments.height, arguments.radius)
    app.run()


if __name__ == '__main__':
    main()