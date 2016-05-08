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
        print("dfs")
        paths = self.dnf_helper_2([self], [], [])
        print(ret_list)
        for p in paths:
            print("path: " + str(p))
        del ret_list[0][0]
        ret_list.reverse()
        ret = ''
        for path in ret_list:
            ret += '('
            for node in path:
                if node == path[-1]:
                    ret += 'n' + str(node)
                else:
                    ret += 'n' + str(node) + '^'
            ret += ')'
            if path != ret_list[-1]:
                ret += 'v'
        
        print ret
        # print 'v'.join(ret_list)
        # self.dnf_helper([], paths)
        # print paths

    def dnf_helper(self, root_val, path, ret_list):
        # if self.label == 1 and node_val != -1:
        #     path.append(node_val)
        #     return 1
        # elif self.label == None and node_val != -1:
        #     path.append(node_val)
        # elif self.label == 0:
        #     path = []
        #     return 0
        # for child in self.children:
        #     node_val += 1
        #     if self.children[child].dnf_helper(node_val, path, ret_list) == 1:
        #         ret = '('
        #         path.reverse()
        #         while len(path) > 0:
        #             item = path.pop()
        #             if len(path) == 0:
        #                 ret += 'n' + str(item)
        #             else:
        #                 ret += 'n' + str(item) + '^'
        #         ret += ')'
        #         ret_list.append(ret)

        stack = []
        stack.append(self)
        while len(stack) > 0:
            node = stack.pop()
            if node.label == None or node.label == 1:
                path.append(node.value)
            if node.label == 1:
                ret_list.append(path)
                path = []
            if self.value != root_val:
                    path.append(self.value)
            for c in node.children:
                stack.append(node.children[c])

    def dnf_helper_2(self, stack, path, ret_path):
        print("root: " + str(self.value))
        print("ret path: " + str(ret_path))
        root = self
        if not(root in path):
            path.append(root)
        for child in root.children:
            if not(root.children[child] in path):
                stack.append(root)
                return root.children[child].dnf_helper_2(stack, path, ret_path)
        #If leaf label is one, save the path
        if root.label == 1:
            print("1 Leaf: " + str(root))
            stack_temp = []
            for val in stack:
                stack_temp.append(val)
            ret_path.append(stack_temp)
            #print("ret path" + str(ret_path))
        last = stack.pop()
        if len(stack) == 0:
            print("ret path: " + str(ret_path))
            return ret_path
        else:
            #return 1
            return last.dnf_helper_2(stack, path, ret_path)

    # def dnf_helper(self, currPath, paths):
    #     # node_val += 1
    #     if self.label == 1:
    #         currPath.append(self.value)
    #         paths.append(currPath)
    #     else:
    #         currPath.append(self.value)
    #         for c in self.children:
    #             self.children[c].dnf_helper(currPath, paths)

### Test cases for dnf ###
n = Node()
n.label = None
n.value = -1
n0 = Node()
n0.label = None
n0.value = 0
n1 = Node()
n1.label = None
n1.value = 1
n2 = Node()
n2.label = 1
n2.value = 2
n3 = Node()
n3.label = 0
n3.value = 3
n4 = Node()
n4.label = 0
n4.value = 4
n5 = Node()
n5.label = None
n5.value = 5
n6 = Node()
n6.label = None
n6.value = 6
n7 = Node()
n7.label = 1
n7.value = 7
n8 = Node()
n8.label = 0
n8.value = 8
n9 = Node()
n9.label = 1
n9.value = 9
n.children = {1: n0, 2: n5}
n0.children = {1: n1, 2: n4}
n1.children = {1: n2, 2: n3}
n5.children = {1: n6, 2: n9}
n6.children = {1: n7, 2: n8}


n.print_dnf_tree()
