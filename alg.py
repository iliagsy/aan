# coding: utf-8
import numpy as np
import numpy.testing as npt
from numpy import double

def get_init_I(nNode):
    return np.random.rand(nNode)

def get_calced_I(H, old_I, alpha=0.85):
    '''
    @param:
    H: shape = (nNode, nNode), dtype = double;
        (H is the original hyperlink matrix)
    old_I: shape = (nNode), dtype = double
    @return: new-round I
    '''
    shape = H.shape
    assert shape[0] == shape[1] and shape[0] == len(old_I)
    nNode = shape[0]
    # Generate row of the matrix I used to add random-click possib.
    # of dangling nodes (correspond to cols in H with all 0s)
    # and the remaining nodes.
    row = np.zeros(nNode, dtype=double)
    Sum = np.add.reduce(H, axis=0)
    row[Sum == 0] = np.add.reduce(old_I[Sum == 0]) * alpha / nNode
    row[Sum != 0] = (1. - alpha) / nNode
    # Now calculate A*old_I
    I = np.zeros(nNode, dtype=double)
    I.flat = np.dot(row, old_I)
    # Add H*old_I, get new-round I
    I += alpha * np.dot(H, old_I)
    # Normalize, make sure sum to 1
    I /= np.add.reduce(I)
    npt.assert_almost_equal(I.sum(), 1)
    return I


def calc_pagerank(H, iter_times=10):
    nNode = H.shape[0]
    I = get_init_I(nNode)
    for i in range(iter_times):
        I = get_calced_I(H, I)
    return I
