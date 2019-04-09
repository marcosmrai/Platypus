#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evolutive operators.

Author: Marcos M. Raimundo <marcosmrai@gmail.com>
        Laboratory of Bioinformatics and Bioinspired Computing
        FEEC - University of Campinas

Based on platypus
"""

import numpy as np
import random, copy
from platypus.core import Variator, Mutation
from platypus import Real

class varOr(Variator):
    def __init__(self, variation, mutation, prVariation, prMutation):
        super(varOr, self).__init__(2)
        self.variation = variation
        self.mutation = mutation
        
        self.prVariation = prVariation
        self.prMutation = prMutation
        
    def evolve(self, parents):
        op_choice = np.random.rand()
        if op_choice<self.prVariation:
            childs = self.variation.evolve(parents)
        elif op_choice<self.prVariation+self.prMutation:
            childs = list(map(self.mutation.evolve, parents))
        else:
            childs = parents
            
        return childs
    

class mutGauss(Mutation):
    def __init__(self, probability = 1., mu=0, sigma=0.1):
        super(mutGauss, self).__init__()
        self.probability = probability
        self.mu = mu
        self.sigma = sigma
        
        
    def mutate(self, parent):
        child = copy.deepcopy(parent)
        problem = child.problem
        probability = self.probability
        
        if isinstance(probability, int):
            probability /= float(len([t for t in problem.types if isinstance(t, Real)]))
            
        for i in range(len(child.variables)):
            if isinstance(problem.types[i], Real):
                if random.uniform(0.0, 1.0) <= probability:
                    child.variables[i] = random.gauss(self.mu, self.sigma)

                    child.evaluated = False
        
        return child
    
    
class cxUniform(Variator):
    def __init__(self, probability = 1.0):
        super(cxUniform, self).__init__(2)
        self.probability = probability
         
    def evolve(self, parents):
        child1 = copy.deepcopy(parents[0])
        child2 = copy.deepcopy(parents[1])
        
        if random.uniform(0.0, 1.0) <= self.probability:
            problem = child1.problem
            nvars = problem.nvars
            
            for i in range(nvars):
                if isinstance(problem.types[i], Real):
                    if random.uniform(0.0, 1.0) <= 0.5:
                        x1 = float(child1.variables[i])
                        x2 = float(child2.variables[i])
                        
                        x1, x2 = x2, x1
                        
                        child1.variables[i] = x1
                        child2.variables[i] = x2
                        child1.evaluated = False
                        child2.evaluated = False
                    
        return [child1, child2]