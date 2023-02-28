# -*- coding: utf-8 -*-
"""finiteSquareWell.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19VTp4Gn816W7U6n_U10hjj2esn8x_Fh9
"""

import numpy as np
from scipy.integrate import odeint, simpson
import matplotlib.pyplot as plt
from scipy.optimize import newton

# CONSTANTS

M = 511 * 1000 # eV
H = 1240 / (2 * np.pi) # eV * nm
A = 1.5 / 2 # nm ; Well Bounds are -A to A
V = 5 # eV

IBV = 0 # initial boundary value
FBV = 0 # final boundary value

def potentialWell(x):
    if x < -A:
        return V
    elif x > A:
        return V
    else: return 0

def ralphODE(yAll, x, L): # y = [y, z] ; L = lambda
    y, z = yAll
    d2ydx2 = [z, y * ((2 * M) / (H**2)) * (potentialWell(x) - L)]
    return d2ydx2

def error(L):
    y0 = [0, .1] # [initial y, initial y']
    x = np.linspace(-1.5, 1.5, 1000)
    y = odeint(ralphODE, y0, x, args=(L,))
    return y[-1, 0] - FBV

def findEigenvalue(seed):
    y0 = [0, .1] # [initial y, initial y']
    k = newton(error, seed) # k = lambda
    x = np.linspace(-1.5, 1.5, 1000)
    y = odeint(ralphODE, y0, x, args=(k,))
    
    func = y[:,0]                                        #takes ALL of the arrays(solutions at each x)
    funcsquared = [n**2 for n in func]                     #squares each entry in the solution

    N = simpson(funcsquared,x)                #integrates using Simpson's rule.  Basically fancy Trapezoid - rule look it up
    y_normalized = np.sqrt(1/N)*func                       #find normalized eigenfunction

    funcsquared = [n**2 for n in y_normalized]             #square normalized eigenfunction
    # Double_Check = simpson(funcsquared,x)     #just check to make sure it really is normalized
    plt.plot(x,funcsquared)                               #plot the squared normalized eigenfunction
    plt.plot([-A, -A], [0, 1], 'k--') 
    plt.plot([A, A], [0, 1], 'k--') # plot a vertical dashed line at the well boundaries
    
    
    funcsquaredWell = [n**2 for n in y_normalized[(x > -A) & (x < A)]]
    prob = simpson(funcsquaredWell, x[(x > -A) & (x < A)]) # # find probability electron is inside the box  by integrating the squared eigenfunction over the interval -A < x < A
    
    return k, prob

seeds = [0.1, 0.5, 1.2, 2, 3, 4.4]
for n in range(6):
    e, p = findEigenvalue(seeds[n])
    print()
    print("n =", n)
    print("Eigenenergy is =", e)
    print("Probability electron found inside box =", p)
    plt.xlabel('Position')
    plt.ylabel('Proability')
    plt.title('Finite Square Well')
    plt.show()