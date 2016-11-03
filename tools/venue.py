# coding: utf-8
'''
用法：作为脚本run，在release/2013/中产生
    sg_venue_network_weight.txt,
        （tab分隔，col1 link to col2, with weight col3）
    sg_venue_network.txt,
    sg_venue_outcites.txt,
    sg_venue_outcites_nonself.txt,
    四个文件
'''
import numpy as np

from consts import base_dir

def map_venue2vid(paper2venue):
    '''
    @param: 从paper_id到venue名字的映射dict
    @return: acl.txt中的paper关联的venue名字到非负id的双向映射，
    （此非负id也作为link matrix中的index）
    '''
    vid_set = set()
    vid_lst = []
    dir_ = base_dir + 'release/2012/acl.txt'
    for line in open(dir_).readlines():
        for pid in line.rstrip().split(' ==> '):
            vid = paper2venue.get(pid)
            if vid not in vid_set:
                vid_lst.append(vid)
                vid_set.add(vid)
    return (dict(zip(vid_lst, range(len(vid_lst)))),
            vid_lst)


def get_venue_link(paper2venue, venue2vid):
    '''
    @return: [(va, vb, n), ...] - va links to vb, n times
    '''
    dir_ = base_dir + 'release/2012/acl.txt'
    linkData = {}
    for line in open(dir_).readlines():
        pid1, pid2 = line.rstrip().split(' ==> ')
        vid1, vid2 = map(paper2venue.get, [pid1, pid2])
        id1, id2 = map(venue2vid.get, [vid1, vid2])
        linkData[(id1, id2)] = linkData.get((id1, id2), 0) + 1
    res_ = sorted(linkData.items(), key=lambda x: x[0])
    res = [(t[0][0], t[0][1], t[1]) for t in res_]
    return res


def get_venue_outcites(with_weight=False, non_self=False):
    '''
    @param:
        with_weight: 考虑同一种引用关系的引用次数(not implemented)
        non_self: 不考虑自我引用
    @return: vid到outcite数的映射
    （默认有自身引用，不考虑引用次数）
    '''
    v2o_dict = {}
    if not with_weight:
        dir_ = base_dir + 'release/2013/sg_venue_network.txt'
        for line in open(dir_).readlines():
            vid1, vid2 = line.rstrip().split(' ==> ')
            if non_self and vid1 == vid2:
                continue
            v2o_dict[int(vid1)] = v2o_dict.get(int(vid1), 0) + 1
    else:
        dir_ = base_dir + 'release/2013/sg_venue_network_weight.txt'
        for line in open(dir_).readlines():
            vid1, vid2, cnt = line.rstrip().split()
            if non_self and vid1 == vid2:
                continue
            v2o_dict[int(vid1)] = v2o_dict.get(int(vid1), 0) + cnt
    return v2o_dict


def map_paper2venue():
    '''
    @return: 从paper_id到venue名字的映射dict
    '''
    dir_ = base_dir + 'release/2012/acl-metadata.txt'
    p2v_map = dict()
    # lol - list of lists
    lol = [p.split('\n') for p in open(dir_).read().split('\n\n')]
    for meta in lol:
        pid, vn = None, None
        for ent in meta:
            if ent.startswith('id ='):
                pid = (ent.split(' = '))[1].strip('{ }')
            if ent.startswith('venue ='):
                vn = (ent.split(' = '))[1].strip('{ }')
        if pid and vn:
            p2v_map[pid] = vn
    return p2v_map


def map_venue2outcite_num(non_self=False):
    v2o_dict = dict()
    dir_ = base_dir + 'release/2013/sg_venue_outcites.txt'
    if non_self:
        dir_ = base_dir + 'release/2013/sg_venue_outcites_nonself.txt'
    for line in open(dir_).readlines():
        vid, num_raw = line.rstrip().split()
        num = int(num_raw)
        v2o_dict[int(vid)] = num
    return v2o_dict


def gen_venue_link_mat(venue2vid, venue2outcite):
    '''
    @return: 公式中的矩阵H
    （不考虑同一种引用关系的引用次数）
    '''
    n_node = len(venue2vid[0])
    linkMat = np.zeros((n_node, n_node))

    dir_ = base_dir + 'release/2013/sg_venue_network.txt'
    for line in open(dir_).readlines():
        vid1, vid2 = line.rstrip().split(' ==> ')
        id1, id2 = int(vid1), int(vid2)
        v1_out = venue2outcite.get(id1)
        linkMat[id2][id1] = 1. / v1_out
    return linkMat


if __name__ == '__main__':
    ############ generate venue link relation file #################
    p2v = map_paper2venue()
    v2v = (map_venue2vid(p2v))[0]
    link_rel = get_venue_link(p2v, v2v)
    link_rel_no_weight = [(t[0], t[1]) for t in link_rel]
    # sg - self-generated
    np.savetxt(base_dir + 'release/2013/sg_venue_network_weight.txt',
               np.array(link_rel),
               fmt='%d')
    np.savetxt(base_dir + 'release/2013/sg_venue_network.txt',
               np.array(link_rel_no_weight),
               delimiter=' ==> ',
               fmt='%d')

    ################# generate venue outcites file ################
    v2o = sorted(get_venue_outcites().items(),
                 key = lambda x: x[0])
    v2o_ns = sorted(get_venue_outcites(non_self=True).items(),
                    key = lambda x: x[0])
    np.savetxt(base_dir + 'release/2013/sg_venue_outcites.txt',
               np.array(v2o),
               fmt='%d')
    np.savetxt(base_dir + 'release/2013/sg_venue_outcites_nonself.txt',
               np.array(v2o_ns),
               fmt='%d')
