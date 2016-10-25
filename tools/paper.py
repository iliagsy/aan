# coding: utf-8
import numpy as np

from consts import base_dir

def map_paper2pid():
    '''
    @return: acl.txt中的paper_id到非负id的映射，
    （此id也作为link matrix中的index）
    '''
    pid_set = set()
    pid_lst = []
    dir_ = base_dir + 'release/2013/acl.txt'
    for line in open(dir_).readlines():
        for pid in line.rstrip().split(' ==> '):
            if pid not in pid_set:
                pid_lst.append(pid)
                pid_set.add(pid)
    return (dict(zip(pid_lst, range(len(pid_lst)))),
            pid_lst)


def map_paper2outcite_num(non_self=False):
    p2o_dict = dict()
    dir_ = base_dir + 'release/2013/paper_outcites.txt'
    if non_self:
        dir_ = base_dir + 'release/2013/paper_outcites_nonself.txt'
    for line in open(dir_).readlines():
        pid, num_raw = line.rstrip().split()
        num = int(num_raw)
        p2o_dict[pid] = num
    return p2o_dict


def gen_paper_link_mat(paper2pid, paper2outcite):
    '''
    @return: 公式中的矩阵H
    '''
    n_node = len(paper2pid[0])
    linkMat = np.zeros((n_node, n_node))

    dir_ = base_dir + 'release/2013/acl.txt'
    for line in open(dir_).readlines():
        pid1, pid2 = line.rstrip().split(' ==> ')
        p1_out = paper2outcite.get(pid1)
        id1, id2 = map(paper2pid.get, [pid1, pid2])
        linkMat[id2][id1] = 1. / p1_out
    return linkMat
