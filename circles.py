import sys
import random
import argparse
import cv2
import numpy as np
from local_search import hill_climbing_with_restarts

class FiguresEvaluation:
    '''
    Represents the objective function.
    Generates the sketch and compares it with the target image.
    '''

    def __init__(self, image):
        self.image = image
        height, width, _ = image.shape
        self.canvas = np.zeros_like(image)
        self.mask = np.zeros((height, width, 1), dtype=np.uint8)

    #TODO: This method should be implemented bu inheritant classes that use other figures
    def _draw_mask(self, figure):
        x, y, r = figure
        cv2.circle(self.mask, (x, y), r, 1, -1)

    def __call__(self, figures):
        self.get_image(figures)
        return np.average(np.sqrt((self.image - self.canvas)**2).sum(2))

    def _add_mask(self):
        avg = cv2.mean(self.image, self.mask[:, :, 0])
        color = np.uint8(avg[:-1]).reshape((1, 1, 3))
        self.canvas *= 1 - self.mask #Remove colors outside the mask
        self.canvas += self.mask * color

    def get_image(self, figures):
        self.canvas.fill(0)
        #Foregorund figures
        for fig in figures:
            self.mask.fill(0)
            self._draw_mask(fig)
            self._add_mask()
        #Background
        self.mask.fill(0)
        for fig in figures:
            self._draw_mask(fig)
        self.mask = 1 - self.mask
        self._add_mask()

        return self.canvas

def random_circle(height, width):
    '''
    Generates a circle with a radius
    no larger thant the largest dimension
    and that always intersects with the area of the image.
    '''
    radius = random.randint(10, max(height, width)) // 2 # The minimum radius could be a parameter
    margin = radius // 2 # This could be a parameter
    return random.randint(-margin, width + margin), random.randint(-margin, height + margin), radius

#TODO: max_figures and neighborhood could be controlled from command line
def generate_sketch(image, evaluations, max_figures=10, neighborhood=10):
    height, width, _ = image.shape
    objective = FiguresEvaluation(image)

    def new_solution():
        ''' Generates a new solution by createing a random sequence of circles'''
        return [random_circle(height, width) for i in range(random.randint(1, max_figures))]

    def neighbor(figures):
        ''' 
        Generates a new solution from another
        by randomly replacing one figure.
        '''
        result = list(figures)
        result[random.randint(0, len(figures) - 1)] = random_circle(height, width)
        return result

    _, solution = hill_climbing_with_restarts(
        objective, neighbor, evaluations, neighborhood, new_solution)
    return objective.get_image(solution)

def arg_parser():
    parser = argparse.ArgumentParser(
        description='Given an image, generates a sketch using just circles')
    parser.add_argument(
        'input',
        help='Path to the image from which the sketch will be generated')
    parser.add_argument('output', help='Path to save the output image')
    parser.add_argument(
        '--figures', '-f',
        nargs='?', default=10, dest='figures', type=int,
        help='Maximum number of figures to be used')
    parser.add_argument(
        '--evaluations', '-e',
        nargs='?', default=100, dest='evaluations', type=int,
        help='Number of sketches to generate in the process')
    return parser

def main():
    args = arg_parser().parse_args()
    image = cv2.imread(args.input)
    if not image:
        print('Could not load image {}'.format(args.input))
        sys.exit(1)
    result = generate_sketch(image, args.evaluations, args.figures)
    cv2.imwrite(args.output, result)

if __name__ == '__main__':
    main()
    