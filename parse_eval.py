#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 16:52:18 2019

@author: yiyuezhuo
"""
import os
from PIL import Image, ImageDraw, ImageFont
fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)


def parse(path):
  with open(path) as f:
    rl = f.readlines()
  
  record_list = []
  record = {'id':None, 'labels':[], 'predictions':[]}
  for line in rl:
    if line.startswith('GROUND TRUTH'):
      record_list.append(record)
      record = {'id':None, 'labels':[], 'predictions':[]}
      record['id'] = line.split(':')[1].strip()
    if line.startswith('label'):
      label = [float(s) for s in line.split(':')[1].split('||')]
      record['labels'].append({'coord': label[:4], 'class':label[4]})
    if line[0].isdigit():
      txt_class, txt_number = line.split(':')[1:]
      p_class = txt_class.strip().split(' ')[0]
      txt_score, txt_coord = txt_number.split(')')
      score = float(txt_score.split('(')[1])
      coord = [float(n) for n in txt_coord.split('||')]
      record['predictions'].append(
          {'coord':coord, 'class':p_class, 'score':score})
  record_list.append(record)
  record_list = record_list[1:]
  
  return record_list

def display_rectangle(record_list, root, target_root, verbose=True):
  for record in record_list:
    path = os.path.join(root, record['id'] + '.jpg')
    im = Image.open(path)
    draw=ImageDraw.Draw(im)
    
    for pred in record['predictions']:
      c = pred['coord']
      xy = [(c[0], c[1]), (c[2], c[3])]
      label = pred['class']

      draw.text((xy[0][0],xy[0][1]-40), label, 
              font=fnt, fill = (255,0,255))
      draw.rectangle(xy, outline=(255,0,255))
      
      target_path = os.path.join(target_root, record['id'] + '.jpg')
      im.save(target_path)
      
      if verbose:
        print('{} -> {}'.format(path, target_path))



record_list = parse('eval/test1.txt')