'''
Created on 12 июл. 2020 г.

@author: elyneagapova
'''
from _elementtree import Element
import 
#get element from dict whith's key is greater then other element's key

def max_for_dicts(elements,key):
    if not elements:
        return
    
    max_key = elements[0][key]
    max_element = elements[0]
    
    for element in elements:
        if element[key] > max_key:
            max_ley = element[key]
            max_element = element
            
    return max_element
    
#get elememts from dict which are greater then man_value by the key (f.e. get messages after fixed time)

def filter_for_dicts(elements, key, min_value):
    new_elements = []
    for element in elements:
        if element[key] >= min_value:
            new_elements.append(element)
    
    return new_elements