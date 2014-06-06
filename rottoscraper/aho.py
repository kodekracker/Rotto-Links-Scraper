#! /usr/bin/python
# coding: utf-8

from collections import deque

class Node :
    def __init__(self, ch=None) :
        self.char = ch
        self.transitions = []
        self.results = []
        self.fail = None

class AhoCorasick :

    def __init__(self) :
        self.terms = []
        self.root = None

    def addKeyword(self, term) :
        self.terms.append(term)

    def makeKeywordTree(self) :
        # Create the root node and queue for failure paths
        root = Node('R')
        root.fail = root
        queue = deque([root])

        # Create the initial tree
        for keyword in self.terms :
            current_node = root
            for ch in keyword :
                new_node = None
                for transition in current_node.transitions:
                    if transition.char == ch:
                        new_node = transition
                        break

                if new_node is None:
                    new_node = Node(ch)
                    current_node.transitions.append(new_node)
                    if current_node is root:
                        new_node.fail = root

                current_node = new_node
            current_node.results.append(keyword)

        # Create failure paths
        while queue:
            current_node = queue.popleft()
            for node in current_node.transitions:
                queue.append(node)
                print 'Add-> ', node.char
                fail_state_node = current_node.fail
                while not any(x for x in fail_state_node.transitions if node.char == x.char) and fail_state_node is not root:
                    fail_state_node = fail_state_node.fail
                    print 'Fail State Node --> ', fail_state_node.char
                node.fail = next((x for x in fail_state_node.transitions if node.char == x.char and x is not node), root)
                print 'Node Fail --> ', node.fail.char
                print
        # tree has been built! return it
        self.root = root

    def searchKeywords(self, text=None) :
        hits = []
        currentNode = self.root

        # Loop through characters
        for c in text :
            # Find next state (if no transition exists, fail function is used)
            # walks through tree until transition is found or root is reached
            trans = None
            while trans == None :
                # trans=currentNode.GetTransition(text[index])
                for x in currentNode.transitions :
                    if x.char == c :
                        trans = x
                if currentNode == self.root : break
                if trans==None : currentNode=currentNode.fail

            if trans != None : currentNode=trans
            # Add results from node to output array and move to next character
            for result in currentNode.results :
                hits.append(result)

        # Convert results to array
        return hits
