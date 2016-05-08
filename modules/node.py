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
        paths = self.dnf_helper([self], [], [])
        ret = ''
        for p in paths:
            del p[0]
            ret += '('
            for i, n in enumerate(p):
                if i == 0:
                    continue
                if n == p[-1]:
                    ret += str(p[i-1].name) + '='
                    for c in p[i - 1].children:
                        if n == p[i-1].children[c]:
                            ret += str(c)
                else:
                    ret += str(p[i-1].name) + '='
                    for c in p[i - 1].children:
                        if n == p[i-1].children[c]:
                            ret += str(c)
                    ret += '^'
            ret += ')'
            if p != paths[-1]:
                ret += 'v'
                
        print ret
        
    def dnf_helper(self, stack, path, ret_path):
        '''
        performs recursion for print_dnf_tree and returns list of lists of nodes
        '''
        root = self
        if not(root in path):
            path.append(root)
        for child in root.children:
            if not(root.children[child] in path):
                stack.append(root)
                return root.children[child].dnf_helper(stack, path, ret_path)
        #If leaf label is one, save the path
        if root.label == 1:
            stack_temp = []
            for val in stack:
                stack_temp.append(val)
            stack_temp.append(root)
            ret_path.append(stack_temp)
        last = stack.pop()
        if len(stack) == 0:
            return ret_path
        else:
            return last.dnf_helper(stack, path, ret_path)
            
### Test cases for dnf ###
# n = Node()
# n.label = None
# n.value = -1
# n0 = Node()
# n0.label = None
# n0.value = 0
# n1 = Node()
# n1.label = None
# n1.value = 1
# n2 = Node()
# n2.label = 1
# n2.value = 2
# n3 = Node()
# n3.label = 0
# n3.value = 3
# n4 = Node()
# n4.label = 0
# n4.value = 4
# n5 = Node()
# n5.label = None
# n5.value = 5
# n6 = Node()
# n6.label = None
# n6.value = 6
# n7 = Node()
# n7.label = 1
# n7.value = 7
# n8 = Node()
# n8.label = 0
# n8.value = 8
# n9 = Node()
# n9.label = 1
# n9.value = 9
# n.children = {1: n0, 2: n5}
# n0.children = {1: n1, 2: n4}
# n1.children = {1: n2, 2: n3}
# n5.children = {1: n6, 2: n9}
# n6.children = {1: n7, 2: n8}