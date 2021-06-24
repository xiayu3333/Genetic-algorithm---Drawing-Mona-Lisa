"""
Draw monalisa picture with ellipses
using genetic algorithm

Created on October, 2020 by XIA, Yu
"""

from PIL import Image, ImageDraw
import numpy as np
import sys
import random

class GA():
    def __init__(self, select, crossover):
        self.select = select
        self.crossover = crossover
    
    
    def wheelSelect(self, evals, candidates, num_seclected = 10):
        """
        wheel selection
        """
        evals = [1 / i for i in evals]   # adjust the evaluation function so as the probability is correct
        return np.random.choice(candidates, size = num_seclected, p = evals / np.sum(evals))
    
    def tournamentSelect(self):
        pass

    def bestSelect(self, evals, candidates):
        #only the best two candidates are choosen as two parents.         
        parent_1 = candidates[evals.index(sorted(evals)[0])] 
        parent_2 = candidates[evals.index(sorted(evals)[1])]

        return parent_1, parent_2


    def fixCrossover(self, parents):
        
        children = np.empty(shape = (1,))
        for parent_x in parents:
            for parent_y in parents:
                child_x, child_y = zip(parent_x, parent_y)
                np.append(children, child_x,child_y)
        return children
    
    def randomCrossover(self, parent_1, parent_2):
        select_matrix = np.random.randint(2, size = parent_1.shape)
        child_1 = parent_1 * select_matrix + parent_2 * (select_matrix^1)
        child_2 = parent_2 * select_matrix + parent_1 * (select_matrix^1)

        return child_1, child_2

    def mutate(self, candidates, rate = 0.5/100):
        pass

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
        
        chromosome = np.random.rand(num_ellipses, 8) *\
                     [width, height, width, height, 255, 255, 255, 255] 
        chromosome = chromosome.astype(int) 
        return chromosome

    def __str__(self):
        return np.fromstring(self)


colour_black= (0, 0, 0)
num_ellipses = 150
num_generations = 10000
num_chromosomes = 48
filepath = "/home/xiayu/Downloads/MonaLisa.png"

imgOrigin = Image.open(filepath).convert('RGB')
width, height = imgOrigin.size


def to_img(chromosome, show=False, save=False):
    size = imgOrigin.size
    img = Image.new('RGB', size, colour_black)
    draw = ImageDraw.Draw(img, 'RGBA')
   
    for ellipse in chromosome:
        points = (ellipse[0], ellipse[1], ellipse[2], ellipse[3])
        colour = (ellipse[4], ellipse[5], ellipse[6], ellipse[7])
        draw.ellipse(points, fill=colour, outline=None)
     
    if show:
        img.show()
        
    if save:
        img.save('result.png')    
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
    #if len(sys.argv) != 2:
    #    sys.exit(0) 
    
    #Step 1: Generate chromosomes as candidates
    candidates = [Chromosome() for i in range(num_chromosomes)]

    ga = GA(select = "bestSelect", crossover = "randomCrossover")
    
    for generation in range(num_generations):
        """
        Reproduction.
        """   

        #Step 2: Evaluate
        evals = [evaluate(imgOrigin, to_img(candidate)) for candidate in candidates]
        
        #Step 3: Select
        parent_1, parent_2 = ga.selection(evals, candidates)
        
        #Step 4: Crossover
        child_1, child_2 = ga.crossover(parent_1, parent_2)
        
        #Step 5: Mutate
        index = random.randrange(num_ellipses)
        child_1[index] = mutate(child_1[index])
        index = random.randrange(num_ellipses)
        child_2[index] = mutate(child_2[index])
        
        #Step 6: Evaluate two parents and two children
        candidates = (parent_1, parent_2, child_1, child_2)
        evals = [evaluate(imgOrigin, to_img(candidate)) for candidate in candidates]
        print("Fitness = ")
        print(evals)
        print(str(generation) + " generations.\n")
     
    #final result
    to_img(child_1, show=True, save=True)

    return sys.exit(0)

if __name__ == "__main__":
   main(sys.argv)    