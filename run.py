import random
from modules.ID3 import *
from modules.parse import *
from modules.pruning import *
from modules.graph import *
from modules.predictions import *
from modules.pickled import *
from modules.parse import *
from modules.node import *
import matplotlib.pyplot as plt

# Import training and validation datasets
TRAINING_SET_PATH = 'data/btrain.csv'
VALIDATION_SET_PATH = 'data/bvalidate.csv'
TEST_SET_PATH = 'data/btest.csv'
data, attr = parse(TRAINING_SET_PATH, True)
validate_data, validate_attr = parse(VALIDATION_SET_PATH, True)

# Train initial tree and print
# Current best values for accuracy are below
tree = ID3(data, attr, 14*[3], 5) 
print 'Question 2'
print 'DNF form of initial tree trained on ' + TRAINING_SET_PATH + ':'
tree.print_dnf_tree()
print '\r\n'

# Prune initial tree and print new tree
pruned_tree = reduced_error_pruning(tree,data,validate_data)
print 'Question 5'
print 'DNF form of reduced-error pruned tree:'
pruned_tree.print_dnf_tree()
print '\r\n'

# Calculate validation accuracy of initial tree and print
print 'Question 7'
print 'Initial tree validation accuracy:'
print(validation_accuracy(tree, validate_data))
print 'Reduced-error pruned tree validation accuracy:'
print(validation_accuracy(pruned_tree, validate_data))
print '\r\n'

#Plotting
#Create learning curve plot
x = []
y = []
z = []
s = data
sample = []
random.seed(10)
random.shuffle(s)
tenth = int(round(len(data) / 10, 0))
for i in range(1,10):
    x.append(i/float(10))
    sample.extend(s[-tenth:])
    del(s[-tenth:])
    tree = ID3(sample, attr, 14*[4], 5) 
    y.append(validation_accuracy(tree, validate_data))
    pruned_tree_loop = reduced_error_pruning(tree,data,validate_data)
    z.append(validation_accuracy(pruned_tree_loop, validate_data))
    
print 'Question 8'
print 'Displaying plots...'
plt.scatter(x,y)
plt.title('Learning Curve on Initial Tree')
plt.xlabel('% of dataset trained on')
plt.ylabel('% accuracy')
plt.show()

plt.scatter(x,z)
plt.title('Learning Curve on Reduced-error Pruned Tree')
plt.xlabel('% of dataset trained on')
plt.ylabel('% accuracy')
plt.show()

print '\r\n'
print 'Question 9'
create_predictions(pruned_tree, TEST_SET_PATH)