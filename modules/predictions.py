import os.path
from operator import xor
from parse import *
import csv

# DOCUMENTATION
# ========================================
# this function outputs predictions for a given data set.
# NOTE this function is provided only for reference.
# You will not be graded on the details of this function, so you can change the interface if 
# you choose, or not complete this function at all if you want to use a different method for
# generating predictions.

def create_predictions(tree, predict):
    '''
    Given a tree and a url to a data_set. Create a csv with a prediction for each result
    using the classify method in node class.
    '''
    data, attr = parse(predict, True)
    predictions = [tree.classify(x) for x in data]
    output = open('output/PS2.csv', 'wb')
    wr = csv.writer(output, quoting=csv.QUOTE_ALL)
    for x in predictions:
        wr.writerow([x])
    print 'Predictions saved to output/PS2.csv'