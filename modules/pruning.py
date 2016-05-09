from node import Node
from ID3 import *
from operator import xor
from copy import deepcopy

# Note, these functions are provided for your reference.  You will not be graded on their behavior,
# so you can implement them as you choose or not implement them at all if you want to use a different
# architecture for pruning.

def reduced_error_pruning(root,training_set,validation_set):
    '''
    take the a node, training set, and validation set and returns the improved node.
    You can implement this as you choose, but the goal is to remove some nodes such that doing so improves validation accuracy.
    '''
    #Depth first search, when you hit a leaf, go to its parent and set that as the leaf with the same label, if validation
    #accuracy improves then keep, otherwise reverse change
    root_copy = deepcopy(root)
    curr_accuracy = validation_accuracy(root_copy, validation_set)
    pruned_tree = pruning_dfs(root_copy, root_copy, [root_copy], [], validation_set, curr_accuracy)
    return pruned_tree

def validation_accuracy(tree,validation_set):
    '''
    takes a tree and a validation set and returns the accuracy of the set on the given tree
    '''
    predictions = [tree.classify(x) for x in validation_set]
    num_correct = 0
    for i in range(len(predictions)):
        if predictions[i] == validation_set[i][0]:
            num_correct += 1
    return num_correct / float(len(predictions))
    
def pruning_dfs(root, subroot, stack, path, validation_set, curr_accuracy):
        '''
        performs recursive dfs and prunes leaves, returns pruned tree
        '''
        if not(subroot in path):
            path.append(subroot)
        for child in subroot.children:
            if not(subroot.children[child] in path):
                stack.append(subroot)
                return pruning_dfs(root, subroot.children[child], stack, path, validation_set, curr_accuracy)
        #If leaf make change and test accuracy
        if len(stack) == 0:
            return root
        #elif subroot.label == 0 or subroot.label == 1:
        else:
            #Save subroot label and parent's children
            label = subroot.label
            parent = stack.pop()
            children = parent.children
            parent.children = {}
            parent.label = label
            #Test validation accuracy of pruned tree
            accuracy = validation_accuracy(root, validation_set)
            #If accuracy worsens, then undo pruning
            if accuracy < curr_accuracy:
                parent.label = None
                parent.children = children
            else:
                curr_accuracy = accuracy
            return pruning_dfs(root, parent, stack, path, validation_set, curr_accuracy)
