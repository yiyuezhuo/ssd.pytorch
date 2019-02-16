# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 09:24:45 2019

@author: yiyuezhuo
"""

from .voc0712 import VOCAnnotationTransform, VOCDetection
import os.path as osp


SWITCH_CLASSES = (  # always index 0
    'open', 'close')

class SWITCHAnnotationTransform(VOCAnnotationTransform):
    def __init__(self, class_to_ind=None, keep_difficult=False):
        self.class_to_ind = class_to_ind or dict(
            zip(SWITCH_CLASSES, range(len(SWITCH_CLASSES))))
        self.keep_difficult = keep_difficult

class SWITCHDetection(VOCDetection):
    def __init__(self, root,
                 transform=None, target_transform=SWITCHAnnotationTransform(),
                 dataset_name='switch'):
        self.root = root
        #self.image_set = image_sets
        self.transform = transform
        self.target_transform = target_transform
        self.name = dataset_name
        self._annopath = osp.join('%s', 'Annotations', '%s.xml')
        self._imgpath = osp.join('%s', 'JPEGImages', '%s.jpg')
        self.ids = list()
        for line in open(osp.join(root, 'ImageSets', 'Main', 'trainval.txt')):
            self.ids.append((root, line.strip()))
