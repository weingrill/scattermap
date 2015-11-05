#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Nov 3, 2015

@author: Joerg Weingrill <jweingrill@aip.de>
'''
import numpy as np
import matplotlib.pyplot as plt

def makecolormap():
    from matplotlib.colors import LinearSegmentedColormap

    cdict  = {'red':   ((0.0, 0.0, 0.0),
                   (0.5, 0.0, 0.0),
                   (0.75, 1.0, 1.0),
                   (1.0, 1.0, 0.0)),

         'green': ((0.0, 0.0, 0.0),
                   (0.25, 1.0, 1.0),
                   (0.5, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 0.0, 0.0),
                   (0.25, 1.0, 1.0),
                   (0.5,1.0,1.0),
                   (0.75, 1.0, 1.0),
                   (1.0, 0.0, 0.0))
            }
    
    
    cyan_red = LinearSegmentedColormap('CyanRed', cdict)
    plt.register_cmap(cmap=cyan_red)

def testcolormap():
    x = np.arange(0, np.pi, 0.1)
    y = np.arange(0, 2*np.pi, 0.1)
    X, Y = np.meshgrid(x, y)
    Z = abs(np.cos(X) * np.sin(Y)) * 20
    
    # Make the figure:
    
    plt.imshow(Z, interpolation='nearest', cmap='CyanRed')
    plt.colorbar()
    plt.show()

class ScatterMap(object):
    '''
    ScatterMap class to read the scattermap files produced with Java
    '''


    def __init__(self, filename, cellsintime = None, cellsinrow = None, pre = " MSSL "):
        '''
        Constructor
        '''
        self.filename = filename
        self.cellsintime = cellsintime
        self.cellsinrow = cellsinrow
        self.pre = pre
        # read the strip from the filename by omitting the last 4 characters
        self.strip=int(filename[-5:-4])
        #automatically load the file
        self.fromfile(filename)
    
    def fromfile(self, filename):
        '''
        load the data from the file and put it into an array
        '''
        # read the file and unpack into three variables
        x, y, z = np.loadtxt(filename, unpack = True)
        # automatically determine the dimensions if not set
        if self.cellsintime is None:
            self.cellsintime = max(x) + 1
        if self.cellsinrow is None:
            self.cellsinrow = max(y) + 1
        # generate an empty array
        self.map = np.zeros([self.cellsintime,self.cellsinrow])
        # convert x and y to int types so we can use them as indices
        x = np.asarray(x, dtype='int')
        y = np.asarray(y, dtype='int')
        # fill up the matrix with values
        self.map[x, y] = z
        # 
        self.map = self.map.transpose()
    
    def show(self, ystart=0, yend=12, xstart=0, xend=360):
        '''
        plot the data
        '''
        extent = (xstart, xend, ystart, yend)
        
        minval = np.min(self.map)
        maxval = np.max(self.map)
        # get the dimensions of the array
        ny, nx = self.map.shape
        print " Min in map is %d" % minval
        print " Max in map is %d" % maxval
        
        #create a figure with white background
        fig = plt.figure(figsize=[12,6], facecolor='white', edgecolor='white')
        ax = fig.add_subplot(111)
        # set the title
        plt.title(self.pre + 'ScatterMap Strip %d' % self.strip)
        # set the label of the x axis
        xlabel = 'Time as sunphase  Background Min %d, Max %d  Grid %d x %d' % \
            (minval, maxval, nx, ny)
        plt.xlabel(xlabel)
        # set the label of the y axis
        plt.ylabel('CCD Row')
        
        print ' Grid has %d cells' % (nx*ny)
        colormap = 'CyanRed'
        ims = plt.imshow(self.map, aspect=18.0, cmap=plt.get_cmap(colormap),
                   origin = 'lower',
                   interpolation='none', vmin=0, vmax=20, extent = extent)
        # we want the tickmarks to point outwards
        plt.tick_params(axis = 'both', which = 'major', direction='out')
        plt.tick_params(axis = 'both', which = 'minor', direction='out')
        #prepare x ticks
        xlocs = np.linspace(0.0, 360.0, 6)
        xticks = ['%.1f' % (x/360.0) for x in xlocs]
        plt.xticks(xlocs, xticks)
        #prepare y ticks (very dirty)
        yticks = 4.0*np.arange(0, ny, (yend-ystart+1))/ny+4
        ylocs = (yend-ystart)*(yticks - 4.0)/4
        
        plt.yticks(ylocs, yticks)
        plt.minorticks_on()
        # we generate the colorbar
        cb = plt.colorbar(ims)
        # I suggest that the units belong to the colorbar
        cb.set_label('e- /pix /4.4s')
        # this is the alternative way to put text on the plot in data coordinates
        #plt.text(360.0, -1.0, 'e- /pix /4.4s')
        
        #remove the borders
        plt.tight_layout()
        #show on screen
        plt.show()
    
    def cumulative_frequency(self):
        # taken from http://stackoverflow.com/questions/15408371/cumulative-distribution-plots-python
        # make the array onedimensionally
        data = np.ravel(self.map)
        # sort the data
        sorted_data = np.sort(data) # Or data.sort(), if data can be modified
        x = sorted_data
        y = np.arange(sorted_data.size)/1000.0
        # Cumulative distributions:
        plt.step(x, y)  # From 0 to the number of data points-1
        # alternatively cumfreqs, lowlim, binsize, extrapoints = scipy.stats.cumfreq(data, numbins=4)
        
        plt.title('Cumulative frequency')
        plt.xlabel('e- /pix /4.4s')
        plt.ylabel('1000 counts')
        plt.xlim(0,100)
        
        # see http://matplotlib.org/examples/pylab_examples/axes_demo.html
        # this is another inset axes over the main axes
        a = plt.axes([0.4, 0.2, .4, .5])
        plt.step(x, y)
        # we want to see minor ticks in the plot, disabled by default
        plt.minorticks_on()
        # set the limits for both axis
        plt.xlim(20, 25)
        plt.ylim(104,109)
        
        plt.savefig('../ScatterMap1_cumfreq.png')
        plt.savefig('../ScatterMap1_cumfreq.pdf')
        plt.show()
        # close the plot gracefully
        plt.close()

if __name__ == '__main__':
    '''
    here is the main routine. Usually not necessery, but makes the file
    importable, where this main part then is not executed.
    '''
    makecolormap()
    sm = ScatterMap('/work2/jwe/Projects/ScatterMap/ScatterMap1.txt')
    sm.cumulative_frequency()
    #sm.show()