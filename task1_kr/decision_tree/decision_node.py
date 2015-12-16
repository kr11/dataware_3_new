# coding:utf-8
__author__ = 'kangrong'

class DecisionTreeNode:
    label = None
    split_value = 0.0
    classify = None
    sub_tree = {}

    def print_node(self,space):
        if self.classify is not None:
            print space+'{'+self.classify+'}'
        else:
            #print space+'{'
            print space+'label:'+self.label
            if self.split_value != 0:
                print space+str(self.split_value)
            for st in self.sub_tree:
                print space+str(st)
                self.sub_tree[st].print_node(space+'    ')
            #print space+'}'
