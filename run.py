# coding: utf-8
'''
最顶层的执行脚本
分别计算paper, author, venue的PR值，
并存到当前路径下的文本文件
'''
# naming convention:
# gen_paper_link_mat(map_paper2pid(),
#                    map_paper2outcite_num(non_self))
import numpy as np

from tools.venue import *
from tools.paper import *
from tools.author import *
from alg import *

def get_n_save_PR(item, non_self=False, iter_times=10):
    assert item in ('paper', 'author', 'venue')
    if item == 'paper':
        H = gen_paper_link_mat(
            map_paper2pid(),
            map_paper2outcite_num(non_self)
        )
    elif item == 'author':
        H = gen_author_link_mat(
            map_author2aid(),
            map_author2outcite_num(non_self)
        )
    elif item == 'venue':
        H = gen_venue_link_mat(
            map_venue2vid(map_paper2venue()),
            map_venue2outcite_num(non_self)
        )
    PR = calc_pagerank(H, iter_times)
    nonself_mark = '_ns' if non_self else ''
    np.savetxt(base_dir + ('%s_PageRankVec%s_%d.txt'
                           % (item, nonself_mark, iter_times)),
               PR,
               fmt='%.5f')
    np.save(base_dir + ('%s_PageRankVec%s_%d.npy'
                        % (item, nonself_mark, iter_times)), PR)


if __name__ == '__main__':
    for item in ('venue', 'paper', 'author'):
        for NS in (False, True):
            for iter_times in range(10, 51, 10):
                get_n_save_PR(item, NS, iter_times)
