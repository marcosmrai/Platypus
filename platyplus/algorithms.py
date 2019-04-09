#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SMS-EMOA implemantation

Author: Marcos M. Raimundo <marcosmrai@gmail.com>
        Laboratory of Bioinformatics and Bioinspired Computing
        FEEC - University of Campinas

Based on platypus
"""
import numpy as np
import pygmo as pg

from platypus import AbstractGeneticAlgorithm, nondominated_sort, ParetoDominance
from platypus import RandomGenerator, TournamentSelector, default_variator

class SMSEMOA(AbstractGeneticAlgorithm):
    
    def __init__(self, problem,
                 population_size = 100,
                 generator = RandomGenerator(),
                 selector = TournamentSelector(2),
                 variator = None,
                 archive = None,
                 selection_method = 'nbr_dom', # hv_contr or nbr_dom
                 **kwargs):
        super(SMSEMOA, self).__init__(problem, population_size, generator, **kwargs)
        self.selector = selector
        self.variator = variator
        self.archive = archive
        self.selection_method = selection_method
        
    def step(self):
        if self.nfe == 0:
            self.initialize()
        else:
            self.iterate()
            
        if self.archive is not None:
            self.result = self.archive
        else:
            self.result = self.population
        
    def initialize(self):
        super(SMSEMOA, self).initialize()
        
        if self.archive is not None:
            self.archive += self.population
        
        if self.variator is None:
            self.variator = default_variator(self.problem)
        
    def iterate(self):
        offspring = []
        
        directions = np.array(self.problem.directions)

        parents = self.selector.select(self.variator.arity, self.population)
        childs = self.variator.evolve(parents)
        child = [np.random.choice(childs)]
        offspring.extend(child)
            
        self.evaluate_all(offspring)
        
        offspring.extend(self.population)
        nondominated_sort(offspring)
        
        last_rank = 0#max([ind.rank for ind in offspring])
        last_front = [i for i,ind in enumerate(offspring) if ind.rank==last_rank]
        
        self.population = []
        while len(self.population)+len(last_front)<self.population_size:
            self.population += [ind for i,ind in enumerate(offspring) if i in last_front]
            
            last_rank+=1
            last_front = [i for i,ind in enumerate(offspring) if ind.rank==last_rank]
        
        while len(self.population)+len(last_front)>self.population_size:
            if self.selection_method=='nbr_dom' and last_rank>0:
                pr = ParetoDominance()
                domtd_sum = [sum([pr(offspring[i], cmp)>0 for cmp in offspring]) for i in last_front]
                last_front_index = np.argmax(domtd_sum)
            else:
                nadir = np.max([np.array(offspring[i].objectives) for i in last_front],axis=0)
                nadir = nadir - abs(nadir)*directions*0.01
                
                hv = pg.hypervolume([np.array(offspring[i].objectives) for i in last_front])
                last_front_index = hv.least_contributor(nadir)
        
            del last_front[last_front_index]
        self.population += [offspring[i] for i in last_front]
        
        if self.archive is not None:
            self.archive.extend(self.population)