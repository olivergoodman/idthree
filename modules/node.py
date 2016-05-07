# DOCUMENTATION
# =====================================
# Class node attributes:
# ----------------------------
# children - a list of 2 nodes if numeric, and a dictionary (key=attribute value, value=node) if nominal.  
#            For numeric, the 0 index holds examples < the splitting_value, the 
#            index holds examples >= the splitting value
#
# label - is None if there is a decision attribute, and is the output label (0 or 1 for
#	the homework data set) if there are no other attributes
#       to split on or the data is homogenous
#
# decision_attribute - the index of the decision attribute being split on
#
# is_nominal - is the decision attribute nominal
#
# value - Ignore (not used, output class if any goes in label)
#
# splitting_value - if numeric, where to split
#
# name - name of the attribute being split on

class Node:
    def __init__(self):
        # initialize all attributes
        self.label = None
        self.decision_attribute = None
        self.is_nominal = None
        self.value = None
        self.splitting_value = None
        self.children = {}
        self.name = None

    def classify(self, instance):
        '''
        given a single observation, will return the output of the tree
        '''
        curr = self
        while curr.children:
            if curr.is_nominal:
                curr = curr.children[instance[curr.decision_attribute]]
            else:
                if instance[curr.decision_attribute] < curr.splitting_value:
                    curr = curr.children[0]
                else:
                    curr = curr.children[1]
        return curr.label
        # if not self.children:
        #     return self.label
        # else:
        #     for child in self.children:
        #         if self.is_nominal:
        #             if self.children[child].splitting_value == instance[self.decision_attribute]:
        #                 self.children[child].classify(instance)
        #     else:
        #         if instance[self.decision_attribute] < self.splitting_value:
        #             self.children[0].classify(instance)
        #         else:
        #             self.children[1].classify(instance)
        #     # matchingChildren = [child for child in self.children if self.children[child].splitting_value == instance[self.decision_attribute]]
        #     # return matchingChildren[0].classify(instance)

    def print_tree(self, indent = 0):
        '''
        returns a string of the entire tree in human readable form
        IMPLEMENTING THIS FUNCTION IS OPTIONAL
        '''
        # Your code here
        pass
        # use self.name to print


    def print_dnf_tree(self):
        '''
        returns the disjunct normalized form of the tree.
        '''
        ret_list = []
        path = []
        self.dnf_helper(-1, path, ret_list)
        print 'v'.join(ret_list)
 
    def dnf_helper(self, node_val, path, ret_list):
        if self.label == 1 and node_val != -1:
            leaf_reached = True
            path.append(node_val)
            ret = '('
            for item in path:
                if item == path[-1]:
                    ret += 'n' + str(item)
                else:
                    ret += 'n' + str(item) + '^'
            ret += ')'
            ret_list.append(ret)
            path = []
            return True
        elif self.label == None and node_val != -1:
            path.append(node_val)
        for child in self.children:
            node_val += 1
            if self.children[child].dnf_helper(node_val, path, ret_list):
                path = []


### Test cases for dnf ###
n = Node()
n.label = None
n0 = Node()
n0.label = 1
n1 = Node()
n1.label = None
n.children = {1: n0, 2: n1}
n2 = Node()
n2.label = 0
n3 = Node()
n3.label = 1
n1.children = {1: n2, 2: n3}
n4 = Node()
n5 = Node()

n.print_dnf_tree()
