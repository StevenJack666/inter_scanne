# import os
# import matplotlib.pyplot as plt
# import numpy as np
# import pygame
#
# pygame.init()
# font = pygame.font.Font('msyh.ttc', 64)
#
#
# def writing(txt, pth):
#     r_txt = font.render(txt, True, (0, 0, 0), (255, 255, 255))
#     pygame.image.save(r_txt, os.path.join(pth, txt + '.jpg'))
#
#
# def indexing(txt):
#     res = []
#     for i in range(len(txt)):
#         try:
#             res.append(standards.index(txt[i] + '\n') + 1)
#         except:
#             new_chrs.append(txt[i])
#             res.append(len(standards) + len(new_chrs) + 1)
#     return res
#
#
# if __name__ == '__main__':
#     pth = 'self_dataset_001'
#
#     f_tr = open(os.path.join(pth, 'train.txt'), encoding='utf-8-sig')
#     f_ts = open(os.path.join(pth, 'test.txt'), encoding='utf-8-sig')
#     f_st = open('label_cn.txt', 'r', encoding='utf-8-sig')
#
#     f_tr2 = open(os.path.join(pth, 'train2.txt'), 'w', encoding='utf-8-sig')
#     f_ts2 = open(os.path.join(pth, 'test2.txt'), 'w', encoding='utf-8-sig')
#
#     train_items = f_tr.readlines()
#     test_items = f_ts.readlines()
#     standards = f_st.readlines()
#     new_chrs = []
#
#     f_tr.close()
#     f_ts.close()
#     f_st.close()
#
#     for i in range(len(train_items)):
#         txt = train_items[i].split(".")[0]
#         idxes = indexing(txt)
#         img = writing(txt, pth)
#
#         cnt = "train_%06d.jpg" % i
#         os.rename(os.path.join(pth, txt + '.jpg'), os.path.join(pth, cnt))
#         for idx in idxes:
#             cnt = cnt + " {}".format(idx)
#         f_tr2.write(cnt + '\n')
#
#     for i in range(len(train_items)):
#         txt = test_items[i].split(".")[0]
#         idxes = indexing(txt)
#         img = writing(txt, pth)
#
#         cnt = "test_%06d.jpg" % i
#         os.rename(os.path.join(pth, txt + '.jpg'), os.path.join(pth, cnt))
#         for idx in idxes:
#             cnt = cnt + " {}".format(idx)
#         f_ts2.write(cnt + '\n')
#
#     fh = open('label_cn.txt', 'a', encoding='utf-8-sig')
#     for nw in new_chrs:
#         fh.write(nw + '\n')
#     fh.close()
