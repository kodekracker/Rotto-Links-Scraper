#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from collections import deque


class Node:
    """
        Represents a single node in keyword tree
    """
    def __init__(self, ch=None):
        self.char = ch
        self.transitions = []
        self.results = []
        self.fail = None


class AhoCorasick:
    """
        Returns a list of keywords matched in a given text
    """
    def __init__(self):
        """
            Initialize class attributes
        """
        self.terms = []
        self.root = None

    def add_keyword(self, term):
        """
            Add keywords
        """
        self.terms.append(term)

    def make_keyword_tree(self):
        """
            Make a keyword tree using keywords
        """
        # Create the root node and queue for failure paths
        root = Node('R')
        root.fail = root
        queue = deque([root])

        # Create the initial tree
        for keyword in self.terms:
            current_node = root
            for ch in keyword:
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
                fail_state_node = current_node.fail
                while not any(x for x in fail_state_node.transitions if node.char == x.char) and fail_state_node is not root:
                    fail_state_node = fail_state_node.fail
                node.fail = next(
                    (x for x in fail_state_node.transitions if node.char == x.char and x is not node), root)
        # tree has been built! return it
        self.root = root

    def search_keywords(self, text=None):
        """
            Returns a  list of matched keywords in given text using keyword
            tree
        """
        hits = []
        currentNode = self.root

        # Loop through characters
        for c in text:
            # Find next state (if no transition exists, fail function is used)
            # walks through tree until transition is found or root is reached
            trans = None
            while trans is None:
                # trans=currentNode.GetTransition(text[index])
                for x in currentNode.transitions:
                    if x.char == c:
                        trans = x
                if currentNode == self.root:
                    break
                if trans is None:
                    currentNode = currentNode.fail

            if trans is not None:
                currentNode = trans
            # Add results from node to output array and move to next character
            for result in currentNode.results:
                hits.append(result)

        # Convert results to array
        return hits
