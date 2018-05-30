# -*- coding: utf-8 -*-

import read_data
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Using sheet 2 for the sake of this demo
SHEET = 2

def cauchy(x, a, b, c):
    """ Define a cauchian distribution function. We're not using
        a high degree polynomial fit, because the calculations would
        be too difficult. Cauchian distribution is the best evalution
        of this data.
    """
    
    return c*(b*np.pi*(1+((x-a)/b)**2))**(-1)


def read(sheet):
    """ Read data and fit a cauchian distribution to data with least 
        squares method.
        
        return: dataframe of data and distribution function
    """
    
    df = read_data.read(sheet-1)
    energy = df['x']
    frequency = df['y']
    
    # Fitting the data with least squares using curve_fit from scipy library
    popt, pcov = curve_fit(cauchy, energy, frequency)
    dist = cauchy(energy, *popt)
    
    return df, dist


def plot_data():
    """ Plots the data and the cauchian distribution.
    """
    
    # Read data
    df, dist = read(SHEET)
    energy, frequency = df['x'], df['y']
    
    # Plot data and distribution
    plt.plot(energy, frequency, 'k.', label='Data')
    
    plt.plot(energy, dist, lw=2, c='r',
             label='Cauchian distribution')
    
    plt.xlabel('Energy (eV)')
    plt.ylabel('Frequency')
    plt.grid(ls='--')
    plt.legend()
    plt.show()


def montecarlo(points):
    """ We're using Monte Carlo integration method for this demo. README
        has some more info on how the method works.
    """
    
    # Read data
    df, dist = read(SHEET)
    energy, frequency = df['x'], df['y']
    popt, pcov = curve_fit(cauchy, energy, frequency) 
    
    # Defining the values of the integration window. Energy (e) values
    # are hand picked from the plot and frequency (f) values are from 0 to
    # the maximum value of the distribution function
    e1, e2 = 44, 56
    f1, f2 = 0, max(dist)
    
    # Initializing some vectors
    inside = [] # Is the point inside the area or not (true = 1, false = 0)
    energies = [] 
    frequencies = []
    
    for i in range(points):
        # Random x value
        x = np.random.uniform(e1, e2)
        energies.append(x)
        
        # Random y value
        y = np.random.uniform(f1, f2)
        frequencies.append(y)
        
        # Check if the random value is inside the area or not and append 
        # inside list with the corresponding value
        if y > cauchy(x, *popt):
            inside.append(False)
        
        else:
            inside.append(True)
    
    # Count the probability (README has some more info on this)
    probability = inside.count(1) / len(inside)
    
    # Using DataFrame again, because it makes the process a bit easier
    mcdf = pd.DataFrame()
    mcdf['x'], mcdf['y'], mcdf['z'] = energies, frequencies, inside
    
    hits_x = mcdf[mcdf['z'] == True]['x']
    hits_y = mcdf[mcdf['z'] == True]['y']
    
    misses_x = mcdf[mcdf['z'] == False]['x']
    misses_y = mcdf[mcdf['z'] == False]['y']
    
    # Plot the method
    plt.plot(energy, dist)
    plt.scatter(hits_x, hits_y, c='blue', s=0.5)
    plt.scatter(misses_x, misses_y, c='red', s=0.5)
    
    plt.title('Monte Carlo integration, N = {}, P = {}'
              .format(points, probability))
    plt.xlabel('Energy (eV)')
    plt.ylabel('Frequency')
    plt.grid(ls='--')
    plt.show()    
    
