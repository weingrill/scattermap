#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Nov 6, 2015

@author: Joerg Weingrill <jweingrill@aip.de>

This is a quick test for the layout of the scattermap

'''

from numpy import random, linspace, arange

import matplotlib.pyplot as plt

scattermap = random.rand(52, 2190)

fig = plt.figure(figsize=[12,6], facecolor='white', edgecolor='white')
ax = fig.add_subplot(111)
plt.ylabel('CCD Row')
imshow = plt.imshow(scattermap, interpolation='nearest', aspect='auto', origin='lower')
colorbar = plt.colorbar(imshow, label='e- /pix /4.4s')
xlocs = linspace(0.0, 2190, 6)
xticks = ['%.1f' % (x/2190) for x in xlocs]
plt.xticks(xlocs, xticks)
ylocs = arange(4)*13
yticks = [4,5,6,7]
plt.yticks(ylocs, yticks)

plt.tight_layout()
plt.show()