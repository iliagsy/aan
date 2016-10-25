# coding: utf-8
import numpy as np

class PageRankGenerator(object):

    def __init__(self, n_node, linkArr):
        self.n_node = n_node
        self.linkArr = linkArr
        self.PRVec = np.random.rand(self.n_node)

    def calc_PR(self):
        pass
