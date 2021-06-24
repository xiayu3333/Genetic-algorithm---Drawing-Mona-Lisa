"""
Draw monalisa picture with polygons(in this case 3 vertices, triangles) 
using genetic algorithm

Created on October, 2020 by XIA, Yu
"""

from PIL import Image, ImageDraw
import numpy as np
import sys
import random

colour_black= (0, 0, 0)
num_polygons = 50
num_generations = 5000
num_chromosomes = 48
filepath = "/home/xiayu/Downloads/MonaLisa.png"

imgOrigin = Image.open(filepath).convert('RGB')
width, height = imgOrigin.size


def to_img(chromosome, show=False, save=False):
    size = imgOrigin.size
    img = Image.new('RGB', size, colour_black)
    draw = ImageDraw.Draw(img, 'RGBA')
   
    for polygon in chromosome:
        points = (polygon[0], polygon[1], polygon[2], polygon[3],polygon[4], polygon[5])
        colour = (polygon[6], polygon[7], polygon[8], polygon[9])
        draw.polygon(points, fill=colour, outline=None)
     

    if show:
        img.show()
        
    if save:
        img.save()    
    return img
    

def evaluate(img_1, img_2):
    eval = 0
    for y in range(0, img_1.size[1]):
        for x in range(0, img_1.size[0]):
            r1, g1, b1 = img_1.getpixel((x, y))
            r2, g2, b2 = img_2.getpixel((x, y))
            #eval += (r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2 
            eval += abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2) 
    return eval 

def select(evals, candidates):
    #Tournament selection, only the best two candidates are choosen as two parents.         
    parent_1 = candidates[evals.index(sorted(evals)[0])] 
    parent_2 = candidates[evals.index(sorted(evals)[1])]

    return parent_1, parent_2

def crossover(parent_1, parent_2):
    #select_matrix = np.ones(shape = parent_1.shape, dtype = int) * [1,1,1,1,1,1,0,0,0,0] 
    #The above matrix does not lead to convergence.
    select_matrix = np.random.randint(2, size = parent_1.shape)
    child_1 = parent_1 * select_matrix + parent_2 * (select_matrix^1)
    child_2 = parent_2 * select_matrix + parent_1 * (select_matrix^1)

    return child_1, child_2

def mutate(row):
    # pick one item and replace it with a random number
        
    colomn = random.randrange(10)
    if colomn in (0, 2, 4):
        row[colomn] = random.randrange(width)
    elif colomn in (1, 3, 5):
        row[colomn] = random.randrange(height)
    else:
        row[colomn] = random.randrange(255)
    return row

def main(arg):
    """
    How to call if using two system arguments: bin/python generate.py <path_to_image>
    """
    #if len(sys.argv) != 2:
    #    sys.exit(0) 
    
    #Step 1: Generate chromosomes as candidates
    candidates = [Chromosome() for i in range(num_chromosomes)]
    
    for generation in range(num_generations):
        """
        Reproduction.
        """   

        #Step 2: Evaluate
        evals = [evaluate(imgOrigin, to_img(candidate)) for candidate in candidates]
        
        #Step 3: Select
        parent_1, parent_2 = select(evals, candidates)
        
        #Step 4: Crossover
        child_1, child_2 = crossover(parent_1, parent_2)
        
        #Step 5: Mutate
        index = random.randrange(num_polygons)
        child_1[index] = mutate(child_1[index])
        index = random.randrange(num_polygons)
        child_2[index] = mutate(child_2[index])
        
        #Step 6: Evaluate two parents and two children
        candidates = (parent_1, parent_2, child_1, child_2)
        evals = [evaluate(imgOrigin, to_img(candidate)) for candidate in candidates]
        print(evals)
        print(str(generation) + " reproductions.\n")
     
    #final result
    to_img(child_1, show=True, save=True)

    return sys.exit(0)

class Chromosome(object):
    def __init__(self):
        pass
        
    def __new__(self):
        """
        Act as a constructor.
        chromosome structure is [x0,y0,x1,y1,x2,y2,r,g,b,alpha] 
           x0, x1, x2 in range(0, width]
           y0, y1, y2 in range(0, height]
           r,g,b,alpha in range (0,255]
        in total there exits 10 items
        """
        chromosome = np.random.rand(num_polygons, 10) \
              * [width, height, width, height, width, height, 255, 255, 255, 255] 
        chromosome = chromosome.astype(int) 
        return chromosome

    def __str__(self):
        return np.fromstring(self)


if __name__ == "__main__":
   main(sys.argv)    