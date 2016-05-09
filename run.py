import random
from modules.ID3 import *
from modules.parse import *
from modules.pruning import *
from modules.graph import *
from modules.predictions import *
from modules.pickled import *
from modules.parse import *
from modules.node import *

# Import training and validation datasets
data, attr = parse("data/test_btrain.csv", True)
validate_data, validate_attr = parse("data/test_bvalidate.csv", True)

# Train initial tree and print
tree = ID3(data, attr, 14*[2], 5) 
print "DNF form of initial tree trained on test_btrain.csv:"
tree.print_dnf_tree()
print "\r\n"

# Calculate validation accuracy of initial tree and print
print "Initial tree validation accuracy:"
print(validation_accuracy(tree, validate_data))
print "\r\n"

# Prune initial tree and print new tree
pruned_tree = reduced_error_pruning(tree,data,validate_data)
print "DNF form of reduced-error pruned tree:"
pruned_tree.print_dnf_tree()
print "\r\n"

print "Reduced-error pruned tree validation accuracy:"
print(validation_accuracy(pruned_tree, validate_data))