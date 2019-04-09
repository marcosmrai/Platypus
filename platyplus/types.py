#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unconstrained real type randomly generated using normal distribution.

Author: Marcos M. Raimundo <marcosmrai@gmail.com>
        Laboratory of Bioinformatics and Bioinspired Computing
        FEEC - University of Campinas

Based on platypus
"""
import random
from platypus import Real

class RealGauss(Real):
    """Represents a floating-point value without bounds.
    
    Attributes
    ----------
    mu : int
        Mean of the generated values.
    sigma: int
        Standard deviation of the generated values.
    """
    
    def __init__(self, mu=0, sigma=1):
        super(RealGauss, self).__init__(-float('inf'), float('inf'))
        self.mu = mu
        self.sigma = sigma
        
    def rand(self):
        return random.gauss(self.mu, self.sigma)
        
    def __str__(self):
        return "Real(%f, %f)" % (self.mu, self.sigma)