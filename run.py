import random
from modules.ID3 import *
from modules.parse import *
from modules.pruning import *
from modules.graph import *
from modules.predictions import *
from modules.pickled import *
from modules.parse import *
from modules.node import *

data, attr = parse("data/test_btrain.csv", True)
print data[0] #first index is winner attribute (T/F)
print attr[0] #first index
tree = ID3(data, attr, 14*[2], 5) 
print tree.print_dnf_tree()

# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
# data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [1, 0.42], [0, 0.51], [1, 0.4]]
# numerical_splits_count = [1, 1]
# n = ID3(data_set, attribute_metadata, numerical_splits_count, 5)

# n.print_dnf_tree()
validate_data, validate_attr = parse("data/test_bvalidate.csv", True)
print(validation_accuracy(tree, validate_data))

pruned_tree = reduced_error_pruning(tree,data,validate_data)
pruned_tree.print_dnf_tree()