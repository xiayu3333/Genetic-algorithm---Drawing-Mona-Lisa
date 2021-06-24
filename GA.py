"""
Draw monalisa picture with ellipses
using genetic algorithm

Created on October, 2020 by XIA, Yu
"""


#Eval with numpy
#.format
#limit standart output


#"Gevent" coroutine

#USE GPU => NUMBA

from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import sys
import random

colour_black = (0, 0, 0)
num_ellipses = 200
num_generations = 2000000
num_chromosomes = 48
x = []  # for ploting
y = []  # for ploting
filepath = "C:/Users/cgoub/OneDrive/Documents/toto/monalisa.jpg"

imgOrigin = Image.open(filepath).convert('RGB')
width, height = imgOrigin.size
aImage = np.array(imgOrigin)
aImage = aImage.astype('int32')


def to_img(chromosome, path="", show=False, save=False):
    size = imgOrigin.size
    img = Image.new('RGB', size, colour_black)
    draw = ImageDraw.Draw(img, 'RGBA')

    for ellipse in chromosome:
        points = (ellipse[0], ellipse[1], ellipse[2], ellipse[3])
        colour = (ellipse[4], ellipse[5], ellipse[6], ellipse[7])
        draw.ellipse(points, fill=colour, outline=colour)

    if show:
        img.show()

    if save:
        img.save(path)
    return img


def evaluate(img_1, img_2):
    eval = 0
    img = np.array(img_2)
    img = img.astype('int32')
    errorMatrix = aImage - img

    #eq = np.count_nonzero(errorMatrix == 0)
    errorMatrix = errorMatrix**2
    eval = np.sum(errorMatrix) #  - (1000 * eq)
    #     for y in range(0, img_1.size[1]):
    #         for x in range(0, img_1.size[0]):
    #             r1, g1, b1 = img_1.getpixel((x, y))
    #             r2, g2, b2 = img_2.getpixel((x, y))
    #             #eval += (r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2
    #             eval += abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)
    return eval


def select(evals, candidates):
    # Selection, only the best two candidates are choosen as two parents.
    parent_1 = candidates[evals.index(sorted(evals)[0])]
    parent_2 = candidates[evals.index(sorted(evals)[1])]

    return parent_1, parent_2


def crossover(parent_1, parent_2):
    # select_matrix = np.ones(shape = parent_1.shape, dtype = int) * [1,1,1,1,1,1,0,0,0,0]
    # The above matrix does not lead to convergence.
    select_matrix = np.random.randint(2, size=parent_1.shape)
    child_1 = parent_1 * select_matrix + parent_2 * (select_matrix ^ 1)
    child_2 = parent_2 * select_matrix + parent_1 * (select_matrix ^ 1)
    
    return child_1, child_2


def mut2(cc):
    newcc = np.random.rand(num_ellipses, 8) *\
            [width, height, width, height, 255, 255, 255, 255]
    newcc = newcc.astype(int)
    mutation_mask = np.random.uniform(size=cc.shape)

    return np.where(mutation_mask < 0.001, cc, newcc)


def mutate(row):
    # pick one item and replace it with a random number

    colomn = random.randrange(8)
    if colomn in (0, 2):
        row[colomn] = random.randrange(width)
    elif colomn in (1, 3):
        row[colomn] = random.randrange(height)
    else:
        row[colomn] = random.randrange(255)
    return row


def main(arg):
    """
    How to call if using two system arguments: bin/python generate.py <path_to_image>
    """
    # if len(sys.argv) != 2:
    #    sys.exit(0)

    # Step 1: Generate chromosomes as candidates
    candidates = [Chromosome() for i in range(num_chromosomes)]

    for generation in range(num_generations):
        """
        Reproduction.
        """

        # Step 2: Evaluate
        evals = [evaluate(imgOrigin, to_img(candidate)) for candidate in candidates]

        # Step 3: Select
        parent_1, parent_2 = select(evals, candidates)

        # Step 4: Crossover
        child_1, child_2 = crossover(parent_1, parent_2)
        
        # Step 5: Mutate
        index = random.randrange(num_ellipses)
        child_1[index] = mutate(child_1[index])
        # index = random.randrange(num_ellipses)
        # child_1[index] = mutate(child_1[index])
        index = random.randrange(num_ellipses)
        child_2[index] = mutate(child_2[index])
        # child_1 = mut2(child_1)
        # child_2 = mut2(child_2)
        # Step 6: Evaluate two parents and two children
        candidates = (parent_1, parent_2, child_1, child_2)
        evals = [evaluate(imgOrigin, to_img(candidate)) for candidate in candidates]

        # show up result after each generation
        if generation % 200 == 0:
            print("Fitness = ")
            print(evals)
            print(str(generation) + " generations.\n")

        if generation % 1000 == 0:
            id1 = evals.index(max(evals))
            to_img(candidates[id1], 'C:/Users/cgoub/OneDrive/Documents/toto/{}.png'.format(generation), show=False,save=True)
            np.savetxt('C:/Users/cgoub/OneDrive/Documents/toto/{}.txt'.format(generation), candidates[id1], delimiter=',')
        x.append(generation)
        y.append(evals[0])
    plt.plot(x, y)

    # final result
    to_img(child_1, 'C:/Users/cgoub/OneDrive/Documents/toto/{}-{}.png'.format("final", 15), show=True, save=True)
    plt.show()
    return sys.exit(0)


class Chromosome(object):
    def __init__(self):
        pass

    def __new__(self):
        """
        Act as a constructor.
        chromosome structure is [x0,y0,x1,y1,x2,y2,r,g,b,alpha]
           x0, x1 in range(0, width)
           y0, y1 in range(0, height)
           r,g,b,alpha in range (0,255]
        in total there exits 10 items
        """

        chromosome = np.random.rand(num_ellipses, 8) * \
                     [width, height, width, height, 255, 255, 255, 255]
        chromosome = chromosome.astype(int)
        return chromosome

    def __str__(self):
        return np.fromstring(self)


if __name__ == "__main__":
    main(sys.argv)