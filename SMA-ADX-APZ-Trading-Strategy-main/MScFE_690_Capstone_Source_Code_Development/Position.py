#!/usr/bin/env python
# coding: utf-8

def order(price, signal):
    
    """ Generating position as buying order and selling order. """
    
    # Creating a position
    position = []
    
    for i in range(len(signal)):
        if signal[i] > 1:
            position.append(0)
        else:
            position.append(1)

    for i in range(len(price['Close'])):
        if signal[i] == 1:
            position[i] = 1
        elif signal[i] == -1:
            position[i] = 0
        else:
            position[i] = position[i-1]
     
    return position