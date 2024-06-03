# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 23:01:16 2024

@author: tyler
"""

import math
import itertools
import matplotlib.pyplot as plt
import time
import csv

cellCoords = ((0, 0, 0), (0.5, 0, 0), (0, 0.5, 0), (0, 0, 0.5))
bounds = 400
latticeParams = 3.65555
radiusMax = 350

distDict = {}
ratioData = []

# breakpoint()
def addToDict(coord, freq):
    distance = math.sqrt(coord[0]**2 + coord[1]**2 + coord[2]**2)
    
    if distance in distDict.keys():
        distDict[distance] += 1 * freq
    else:
        distDict[distance] = 1 * freq

start = time.time()
for coord in list(itertools.product(range(1, bounds+1),range(1, bounds+1),range(1, bounds+1))):
    for i in cellCoords:
        partCoord = tuple(map(lambda x, y: latticeParams * (x + y), coord, i))
        addToDict(partCoord, 8)
        

for coord in list(itertools.product(range(1, bounds+1),range(1, bounds+1))):
    for i in cellCoords:
        
        partCoord = (tuple(map(lambda x, y: latticeParams * (x + y), (coord[0], coord[1], 0), i)),
                     tuple(map(lambda x, y: latticeParams * (x + y), (coord[0], 0, coord[1]), i)),
                     tuple(map(lambda x, y: latticeParams * (x + y), (0, coord[0], coord[1]), i)))
        
        for k in partCoord:
            
            if 0 in k:
                addToDict(k, 4)
            else:
                addToDict(k, 8)
            

for coord in range(1, bounds+1):
    for i in cellCoords:
        partCoord = (tuple(map(lambda x, y: latticeParams * (x + y), (coord, 0, 0), i)),
                     tuple(map(lambda x, y: latticeParams * (x + y), (0, coord, 0), i)),
                     tuple(map(lambda x, y: latticeParams * (x + y), (0, 0, coord), i)))
        for k in partCoord:
            
            if k.count(0) == 2:
                addToDict(k, 2)
            else:
                addToDict(k, 4)
                


for i in cellCoords[1:]:
    addToDict(tuple(x*latticeParams for x in i), 4)

end = time.time()
print('Coord generation took ' + str(end-start) + ' s.')

#%%
for r in range(1, radiusMax+1):

    volSingle = (4/3) * math.pi * r**3
    volSum = volSingle
    
    for dist, freq in distDict.items():
        if 2*r > dist:

            volSum += freq * ((math.pi/12) * (4*r + dist)*(2*r - dist)**2)
    
    ratioData.append(volSingle/volSum)

end = time.time()
print('Total calculation took ' + str(end-start) + ' s.')

plt.plot(range(1, radiusMax+1), ratioData)
plt.yscale('log')

#%%

outfile = open('350RadiusData', 'w', newline='')
out = csv.writer(outfile)
out.writerows(map(lambda x: [x], ratioData))
outfile.close()