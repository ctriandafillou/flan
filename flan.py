#!/usr/bin/python
"""
Functions for parsing and plotting anisotropy data from the Horiba Fluorolog 3
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import Image

def spectrum_plot(fname, species):
    """Generate a emission spectrum (wavelength vs. intensity)
    
    Parse spectrum output from the Horiba Fluorolog-3 (in csv format) and return a matplotlib plot (axes object)
    of the data. species is the name of the molecular species. 
    """
    data = np.loadtxt(fname, skiprows=2)
    wv = data[:, 0]
    intensity = data[:, 1]
    
    fig, ax = plt.subplots(figsize=[15,5])
    plt.plot(wv, intensity)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity')
    plt.title("%s Emission Spectrum" % species)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    return fig, ax

def timecourse_plot(fname, species, temp, fit):
    """Generate a time vs. anisotropy plot for a particular temperature.
    
    Parse timecourse output from the Horiba Fluorolog-3 (in csv format) and return a matplotlib plot (fig, axes object)
    of the data. species -> name of the molecular species; temp -> temperature at which the measurement was made.
    """
    data = np.loadtxt(fname, skiprows=2)
    time = data[:, 0]  
    anisotropy = data[:, 1]
    
    fig, ax = plt.subplots(figsize=(10,10))
    ax.scatter(time, anisotropy)
    plt.title('%s Anisotropy vs. time (%d C)' % (species, temp))
    plt.ylabel('Anisotropy')
    plt.xlabel('Time (s)')
    # Uncomment and change to make plots with uniform axes
    #plt.ylim(0.10, 0.35)
    if fit:
        ax.plot(time, np.poly1d(np.polyfit(time, anisotropy, 1))(time))
        print 'Linear fit parameters: '+ str(np.polyfit(time, anisotropy, 1))
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    #print 'Range: ' + str(np.max(anisotropy) - np.min(anisotropy))
    #print 'Mean: %f +/- %f' % (np.mean(anisotropy), np.std(anisotropy))
    return fig, ax

def an_timepoint(fname):
    """Generate an anisotropy single point value based on four individual measurements.
    
    Return both the value and the precision (standard deviation). fname is a single file containing anisotropy data.
    """
    data = np.loadtxt(fname, skiprows=2)
    an = np.mean(data[:, 1])
    er = np.std(data[:, 1])
    return an, er

def an_timepoints(fname):
    """Return individual measurements for a single timepoint"""
    data = np.loadtxt(fname, skiprows=2)
    return data[:, 1]
    
def show_figure(fname):
    """Display a PNG image"""
    fig = Image(filename=(fname))
    fig
    
def generate_fit(x, y, power):
    """Return the fit for an anisotropy timeseries.
    
    Usage: x = time (1D numpy array), y = anisotropy (1D numpy array), power = degree of polynomial in polynomial fit (integer).
    axis.plot(x, generate_fit(x, y, power))
    
    More details: generates a polynomial least squares fit of degree power (the polyfit function returns the coefficients of this fit), then the poly1d function generates this function (takes coefficients as input) and returns the function evaluated at x = time where time is a 1D numpy array. In this way the fit is only plotted on the datapoints.
    """
    return np.poly1d(np.polyfit(x, y, power))(x)

