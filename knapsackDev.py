# -*- coding: utf-8 -*-

import time
import json
import copy

def checkCapacity(contents,knapsack_cap):
    """ contents is expected as a dictionaryof the form {item_id:(volume,value), ...} """
    """ This function returns True if the knapsack is within capacity; False if the knapsack is overloaded """
    load = 0
    if isinstance(contents,dict):
        for this_key in contents.keys():
            load = load + contents[this_key][0]
        if load <= knapsack_cap:
            return True
        else:
            return False
    else:
        print("function checkCapacity() requires a dictionary")

def knapsack_value(items):
    value = 0.0
    if isinstance(items,dict):
        for this_key in items.keys():
            value = value + items[this_key][1]
        return(value)
    else:
        print("function knapsack_value() requires a dictionary")

def getData():
    #f = open('knapsack_test.json','r')
    f = open('knapsack.json','r')
    x = json.load(f)
    f.close()
    for i in range(len(x)):
        myData = x[i]['data']
        x[i]['data'] = {}
        for j in range(len(myData)):
            x[i]['data'][j] = tuple(myData[j]) 
    return x

def loadKnapsack(items,knapsack_cap):
    """ You write this function which is your heuristic knapsack algorithm
    
        Indicate items to be included in the backpack by including their dictionary keys within 
        a list data structure and, subsequently, returning that list of IDs from this function  """
        
    """ Compute existing load in knapsack """
    myUsername = 'aineko' # always return this variable as the first item
    nickname = 'aineko' # This idenfier will appear on the leaderboard, if you desire to be identified.  This may be left as an empty string.
    items_to_pack = []    # use this list for the indices of the items you load into the knapsack
    
    load = 0.0            # use this variable to keep track of how much volume is already loaded into the backpack
    value = 0.0           # value in knapsack


    #extract volumes and values into vectors so we can cleanly iterate over them
    volume = []
    value = []
    for i in range(len(items)):
        volume.append(int(items[i][0]))
        value.append(int(items[i][1]))
    print("knapsack total value (recursive)= ", recursive_knapsack(knapsack_cap, volume, value, len(items)))
    print("dynamic total value (dynamic)= ", dynamic_knapsack(int(knapsack_cap), volume, value, len(items), items_to_pack)) #hack
    print("Items added to list:", items_to_pack)

    item_keys = [k for k in items.keys()]
    pack_item = item_keys[0]
    items_to_pack.append(pack_item)
    #load += items[pack_item][0]
    #value += items[pack_item][1]
    
    return myUsername, nickname, items_to_pack       # use this return statement when you have items to load in the knapsack


def recursive_knapsack(knapsack_cap, volume, value, n):
    #base case
    if n == 0 or knapsack_cap == 0 :
        return 0
    #recursive case; pack the item if volume is less than capacity
    if (volume[n-1] > knapsack_cap):
        return recursive_knapsack(knapsack_cap, volume, value, n-1)
    #determine if we pack the nth item
    else:
        res = max(value[n-1] + recursive_knapsack(knapsack_cap-volume[n-1], volume, value, n-1),
                  recursive_knapsack(knapsack_cap, volume, value, n-1))
        return res

def dynamic_knapsack(knapsack_cap, volume, value, n, packed_elements):
    #create a 2D dynamic table that we populate bottom-up
    dynamic_table = [[0 for w in range(knapsack_cap + 1)] for i in range(n + 1)]

    for i in range(n + 1):
        for j in range(knapsack_cap + 1):
            if i == 0 or j == 0:
                dynamic_table[i][j] = 0
            elif volume[i - 1] <= j:
                dynamic_table[i][j] = max(value[i - 1] + dynamic_table[i - 1][j - volume[i - 1]],
                                          dynamic_table[i - 1][j])
            else:
                dynamic_table[i][j] = dynamic_table[i - 1][j]

    # this is our total value in the knapsack
    res = dynamic_table[n][knapsack_cap]
    #print(res)
    value_copy = value.copy()
    temp = res
    j = knapsack_cap
    #iterate back through to get the elements we stored (not elegant but works)
    for i in range(n, 0, -1):
        if temp <= 0:
            break
        if temp == dynamic_table[i - 1][j]:
            continue
        else:
            #find the index of the element we wish to add to the knapsack
            index = value_copy.index(value[i-1])
            #handle lists with duplicate values and increment our index
            if index in packed_elements:
                while index in packed_elements:
                    index = value_copy.index(value[i-1], index+1)
            packed_elements.append(index)
            #print("index ", index, "added with value = ", value[i-1], " and volume = ", volume[i-1])

            #deduct item's value and volumes from the total remaining
            temp = temp - value[i - 1]
            j = j - volume[i - 1]
    return res

""" Main code """
""" Get data and define problem ids """
probData = getData()
problems = range(len(probData))
silent_mode = True    # use this variable to turn on/off appropriate messaging depending on student or instructor use
""" Error Messages """
error_bad_list_key = """ 
A list was received from load_knapsack() for the item numbers to be loaded into the knapsack.  However, that list contained an element that was not a key in the dictionary of the items that were not yet loaded.   This could be either because the element was non-numeric, it was a key that was already loaded into the knapsack, or it was a numeric value that didn't match with any of the dictionary keys. Please check the list that your load_knapsack function is returning. It will be assumed that the knapsack is fully loaded with any items that may have already been loaded and a score computed accordingly. 
"""
error_response_not_list = """
load_knapsack() returned a response for items to be packed that was not a list.  Scoring will be terminated   """

for problem_id in problems:
    in_knapsack = {}
    knapsack_cap = probData[problem_id]['cap']
    items = probData[problem_id]['data']
    errors = False
    response = None
    
    startTime = time.time()
    team_num, nickname, response = loadKnapsack(items,knapsack_cap)
    execTime = time.time() - startTime
    if isinstance(response,list):
        for this_key in response:
            if this_key in items.keys():
                in_knapsack[this_key] = items[this_key]
                del items[this_key]
            else:
                errors = True
                status = 'Problem ' + str(problem_id) + ' solution references invalid key'
                if not silent_mode:
                    print('Problem ' + str(problem_id) + ' solution references invalid key')
                
    else:
        errors = True
        status = 'Problem ' + str(problem_id) + " is not a list"
        if silent_mode:
            print(error_response_not_list)
                
    if errors == False:
        knapsack_ok = checkCapacity(in_knapsack,knapsack_cap)
        if knapsack_ok:
            knapsack_result = knapsack_value(in_knapsack)
            print('Problem ' + str(problem_id) + ' knapsack loaded within capacity with value ' + str(knapsack_result))
            print('  Execution time:', execTime, ' seconds\n')
        else:
            print('Problem ' + str(problem_id) + ' knapsack overloaded')
    else:
        print(status)