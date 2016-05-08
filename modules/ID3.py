import math
from node import Node
import sys

def ID3(data_set, attribute_metadata, numerical_splits_count, depth):
    '''
    See Textbook for algorithm.
    Make sure to handle unknown values, some suggested approaches were
    given in lecture.
    ========================================================================================================
    Input:  A data_set, attribute_metadata, maximum number of splits to consider for numerical attributes,
    maximum depth to search to (depth = 0 indicates that this node should output a label)
    ========================================================================================================
    Output: The node representing the decision tree learned over the given data set
    ========================================================================================================

    '''
    if not data_set:
        return Node()
    elif check_homogenous(data_set) != None:
        n = Node()
        n.label = check_homogenous(data_set)
        return n
    elif not attribute_metadata:
        n = Node()
        n.label = mode(data_set)
        return n
    elif depth == 0:
        n = Node()
        n.label = mode(data_set)
        return n
    else:
        best, split_value = pick_best_attribute(data_set, attribute_metadata, numerical_splits_count)
        if attribute_metadata[best]['is_nominal'] == False:
            numerical_splits_count[best] -= 1
        if best == False:
            return Node()
        tree = Node() #the root 
        tree.is_nominal = attribute_metadata[best]['is_nominal']
        tree.decision_attribute = best
        tree.splitting_value = split_value
        tree.name = attribute_metadata[best]['name']
        tree.label = None
        data_sub = []
        #if a nominal attribute
        if attribute_metadata[best]['is_nominal'] == True:
            best_attributes_dict = split_on_nominal(data_set, best)
            for v in best_attributes_dict:
                subtree = ID3(best_attributes_dict[v], attribute_metadata, numerical_splits_count, depth - 1)
                subtree.label = mode(best_attributes_dict[v])
                tree.children[v] = subtree #adding branch to the tree
        #if numerical attribute
        else:
            splits = split_on_numerical(data_set, best, split_value)
            for v in splits:
                subtree = ID3(v, attribute_metadata, numerical_splits_count, depth - 1)
                subtree.label = mode(v)
                tree.children[splits.index(v)] = subtree #adding branch to the tree

        return tree

        # NOTES:
        # - need to add depth check
        # - right now: for numerical attr, looping thru ALL attr. Maybe try just the ones form first list ?
        # getting 'pop index out of range', perhaps related to depth check?


        

def check_homogenous(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the output value (index 0) is the same for all examples in the the data_set, if so return that output value, otherwise return None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
     '''
    for attribute in data_set:
        if attribute != data_set[0]:
            return None
    return data_set[0][0]
# ======== Test Cases =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  None
# data_set = [[0],[1],[None],[0]]
# check_homogenous(data_set) ==  None
# data_set = [[1],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  1

def pick_best_attribute(data_set, attribute_metadata, numerical_splits_count):
    '''
    ========================================================================================================
    Input:  A data_set, attribute_metadata, splits counts for numeric
    ========================================================================================================
    Job:    Find the attribute that maximizes the gain ratio. If attribute is numeric return best split value.
            If nominal, then split value is False.
            If gain ratio of all the attributes is 0, then return False, False
            Only consider numeric splits for which numerical_splits_count is greater than zero
    ========================================================================================================
    Output: best attribute, split value if numeric
    ========================================================================================================
    '''
    best_ratio = 0
    best_attribute = False
    steps = 1
    split_value = False
    for i in range(len(attribute_metadata)):
        if attribute_metadata[i]['name'] != 'winner':
            if attribute_metadata[i]['is_nominal'] == True:
                ratio = gain_ratio_nominal(data_set, i)
            else:
                if numerical_splits_count[i] <= 0:
                    continue
                ratio, threshold = gain_ratio_numeric(data_set, i, steps)
            if ratio > best_ratio:
                best_ratio = ratio
                best_attribute = i
                if attribute_metadata[i]['is_nominal'] == False:
                    split_value = threshold
                    
    return best_attribute, split_value

# # ======== Test Cases =============================
# numerical_splits_count = [20,20]
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
# data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, 0.51)
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "weather",'is_nominal': True}]
# data_set = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, False)

# Uses gain_ratio_nominal or gain_ratio_numeric to calculate gain ratio.

def mode(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Takes a data_set and finds mode of index 0.
    ========================================================================================================
    Output: mode of index 0.
    ========================================================================================================
    '''
    #Create list of only the winner variable
    winners = []
    for sublist in data_set:
        winners.append(sublist[0])
    return max(set(winners), key=winners.count)
# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# mode(data_set) == 1
# data_set = [[0],[1],[0],[0]]
# mode(data_set) == 0

def entropy(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Calculates the entropy of the attribute at the 0th index, the value we want to predict.
    ========================================================================================================
    Output: Returns entropy. See Textbook for formula
    ========================================================================================================
    '''
    #Create list of only the winner variable
    winners = []
    for sublist in data_set:
        winners.append(sublist[0])
    entropy = 0
    length = float(len(winners))
    unique_data_set = list(set(winners))
    for x in unique_data_set:
        entropy -= (winners.count(x) / length) * math.log((winners.count(x) / length), 2)
    return entropy

# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[0],[1],[1],[1]]
# entropy(data_set) == 0.811
# data_set = [[0],[0],[1],[1],[0],[1],[1],[0]]
# entropy(data_set) == 1.0
# data_set = [[0],[0],[0],[0],[0],[0],[0],[0]]
# entropy(data_set) == 0


def gain_ratio_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  Subset of data_set, index for a nominal attribute
    ========================================================================================================
    Job:    Finds the gain ratio of a nominal attribute in relation to the variable we are training on.
    ========================================================================================================
    Output: Returns gain_ratio. See https://en.wikipedia.org/wiki/Information_gain_ratio
    ========================================================================================================
    '''
    info_gain = entropy(data_set)
    intr_value = 0
    #Create list of only the attribute variable
    attr = []
    for sublist in data_set:
        attr.append(sublist[attribute])
    length = float(len(attr))
    unique_attr = list(set(attr))
    for value in unique_attr:
        attr_data = []
        for row in data_set:
            if row[attribute] == value:
                attr_data.append(row)
        info_gain -= ((attr.count(value) / length) * entropy(attr_data))
        intr_value -= (attr.count(value) / length) * math.log((attr.count(value) / length), 2)
    return info_gain / intr_value
# ======== Test case =============================
# data_set, attr = [[1, 2], [1, 0], [1, 0], [0, 2], [0, 2], [0, 0], [1, 3], [0, 4], [0, 3], [1, 1]], 1
# gain_ratio_nominal(data_set,attr) == 0.11470666361703151
# data_set, attr = [[1, 2], [1, 2], [0, 4], [0, 0], [0, 1], [0, 3], [0, 0], [0, 0], [0, 4], [0, 2]], 1
# gain_ratio_nominal(data_set,attr) == 0.2056423328155741
# data_set, attr = [[0, 3], [0, 3], [0, 3], [0, 4], [0, 4], [0, 4], [0, 0], [0, 2], [1, 4], [0, 4]], 1
# gain_ratio_nominal(data_set,attr) == 0.06409559743967516

def gain_ratio_numeric(data_set, attribute, steps):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, and a step size for normalizing the data.
    ========================================================================================================
    Job:    Calculate the gain_ratio_numeric and find the best single threshold value
            The threshold will be used to split examples into two sets
                 those with attribute value GREATER THAN OR EQUAL TO threshold
                 those with attribute value LESS THAN threshold
            Use the equation here: https://en.wikipedia.org/wiki/Information_gain_ratio
            And restrict your search for possible thresholds to examples with array index mod(step) == 0
    ========================================================================================================
    Output: This function returns the gain ratio and threshold value
    ========================================================================================================
    '''
    #Create list of only the attribute variable
    attr = []
    for sublist in data_set:
        attr.append(sublist[attribute])
        
    length = float(len(attr))
    best_threshold = None
    best_ratio = 0
    index = 0
    while index < length:
        info_gain = entropy(data_set)
        intr_value = 0
        threshold = attr[index]
        for value in ['>=', '<']:
            attr_data = []
            for row in data_set:
                if (value == '>=' and row[attribute] >= threshold) or (value == '<' and row[attribute] < threshold):
                    attr_data.append(row)
            if len(attr_data) != 0:
                info_gain -= ((len(attr_data) / length) * entropy(attr_data))
                intr_value -= (len(attr_data) / length) * math.log((len(attr_data) / length), 2)

        if intr_value == 0:
            info_ratio = 0
        else:
            info_ratio = info_gain / intr_value
            
        if info_ratio > best_ratio:
            best_ratio = info_ratio
            best_threshold = threshold
        index = index + steps
    
    return best_ratio, best_threshold
# ======== Test case =============================
# data_set,attr,step = [[0,0.05], [1,0.17], [1,0.64], [0,0.38], [0,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 2
# gain_ratio_numeric(data_set,attr,step) == (0.31918053332474033, 0.64)
# data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 4
# gain_ratio_numeric(data_set,attr,step) == (0.11689800358692547, 0.94)
# data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 1
# gain_ratio_numeric(data_set,attr,step) == (0.23645279766002802, 0.29)

def split_on_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  subset of data set, the index for a nominal attribute.
    ========================================================================================================
    Job:    Creates a dictionary of all values of the attribute.
    ========================================================================================================
    Output: Dictionary of all values pointing to a list of all the data with that attribute
    ========================================================================================================
    '''
    subsets = {}
    for row in data_set:
        if row[attribute] not in subsets:
            subsets[row[attribute]] = [row]
        else:
            subsets[row[attribute]].append(row)
    return subsets
# ======== Test case =============================
# data_set, attr = [[0, 4], [1, 3], [1, 2], [0, 0], [0, 0], [0, 4], [1, 4], [0, 2], [1, 2], [0, 1]], 1
# split_on_nominal(data_set, attr) == {0: [[0, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3]], 4: [[0, 4], [0, 4], [1, 4]]}
# data_set, attr = [[1, 2], [1, 0], [0, 0], [1, 3], [0, 2], [0, 3], [0, 4], [0, 4], [1, 2], [0, 1]], 1
# split on_nominal(data_set, attr) == {0: [[1, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3], [0, 3]], 4: [[0, 4], [0, 4]]}

def split_on_numerical(data_set, attribute, splitting_value):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, threshold (splitting) value
    ========================================================================================================
    Job:    Splits data_set into a tuple of two lists, the first list contains the examples where the given
    attribute has value less than the splitting value, the second list contains the other examples
    ========================================================================================================
    Output: Tuple of two lists as described above
    ========================================================================================================
    '''
    subsets = [],[]
    for row in data_set:
        if row[attribute] < splitting_value:
            subsets[0].append(row)
        else:
            subsets[1].append(row)
    return subsets
# ======== Test case =============================
# d_set,a,sval = [[1, 0.25], [1, 0.89], [0, 0.93], [0, 0.48], [1, 0.19], [1, 0.49], [0, 0.6], [0, 0.6], [1, 0.34], [1, 0.19]],1,0.48
# split_on_numerical(d_set,a,sval) == ([[1, 0.25], [1, 0.19], [1, 0.34], [1, 0.19]],[[1, 0.89], [0, 0.93], [0, 0.48], [1, 0.49], [0, 0.6], [0, 0.6]])
# d_set,a,sval = [[0, 0.91], [0, 0.84], [1, 0.82], [1, 0.07], [0, 0.82],[0, 0.59], [0, 0.87], [0, 0.17], [1, 0.05], [1, 0.76]],1,0.17
# split_on_numerical(d_set,a,sval) == ([[1, 0.07], [1, 0.05]],[[0, 0.91],[0, 0.84], [1, 0.82], [0, 0.82], [0, 0.59], [0, 0.87], [0, 0.17], [1, 0.76]])