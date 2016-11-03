# coding: utf-8
import numpy as np

from consts import base_dir

def map_author2aid():
    '''
    @return: author_citation_network.txt中的author_id到非负id的映射，
    （此id也作为link matrix中的index）
    '''
    aid_set = set()
    aid_lst = []
    dir_ = base_dir + 'release/2013/author_citation_network.txt'
    for line in open(dir_).readlines():
        for aid in line.rstrip().split(' ==> '):
            if aid not in aid_set:
                aid_lst.append(aid)
                aid_set.add(aid)
    return (dict(zip(aid_lst, range(len(aid_lst)))),
            aid_lst)


def map_author2outcite_num(non_self=False):
    a2o_dict = dict()
    dir_ = base_dir + 'release/2013/author_outcites.txt'
    if non_self:
        dir_ = base_dir + 'release/2013/author_outcites_nonself.txt'
    for line in open(dir_).readlines():
        aid, num_raw = line.rstrip().split()
        num = int(num_raw)
        if num == 0:
            continue
        a2o_dict[aid] = num
    return a2o_dict


def gen_author_link_mat(author2aid, author2outcite):
    '''
    @return: 公式中的矩阵H
    '''
    n_node = len(author2aid[0])
    linkMat = np.zeros((n_node, n_node))

    dir_ = base_dir + 'release/2013/author_citation_network.txt'
    for line in open(dir_).readlines():
        aid1, aid2 = line.rstrip().split(' ==> ')
        a1_out = author2outcite.get(aid1, np.inf)
        id1, id2 = map(author2aid[0].get, [aid1, aid2])
        linkMat[id2][id1] = 1. / a1_out
    return linkMat
