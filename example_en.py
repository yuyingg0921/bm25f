#!/usr/bin/env python
# coding: utf-8

import BM25F.core
import BM25F.en
import BM25F.exp
import sys

tokenizer = BM25F.en.Tokenizer(token_filter=BM25F.en.TokenFilter())

bj = BM25F.exp.bag_jag()
bj_list = []

d = {}

line_num = 0

for i in range(0,5):
    with open("iek/document_"+str(i)) as f:
        tmp = ''
        d['_id'] = str(i)
        d['body'] = ''
        for line in f:   
            line_num += 1
            if line_num == 1:
                d['title'] = line.strip()
            elif line_num == 2:
                d['abstract'] = line.strip()
            else:
                tmp = d['body']
                d['body'] = tmp + line
        line_num = 0
        bj.append(BM25F.exp.bag_dict().read(tokenizer, d))
        bj_list.append(BM25F.exp.bag_dict().read(tokenizer, d))


'''
bj.append(bd0)


bd1 = BM25F.exp.bag_dict().read(tokenizer, {
    '_id': '1',
    'title': 'd1',
    'body': 'Silicon photonics is a broad term that refers to the semiconductor industry’s efforts to bring optical components into or closer to today’s silicon computer chips, which trade in electrons. Photonic components can carry more data farther and faster, without heating up and without degradation in the signal.',
})


bd2 = BM25F.exp.bag_dict().read(tokenizer, {
    '_id': '2',
    'title': 'Silicon Photonic Test Document',
    'body': 'Experts following the company say Magic Leap seems to be taking a gamble on silicon photonics because the technology would dramatically improve the augmented-reality display. Typical augmented-reality goggles use mirrors and beam splitters to reflect images from a microdisplay into the eye. These systems also let in light from the real world. They can achieve a 3-D effect by simultaneously showing slightly different images to the right and left eyes. This is called stereoscopic 3-D, and even though today it’s done with moving images produced by LCDs rather than the static photos used in the 19th century, it’s a technology with major limitations. Being confronted with left and right images that appear to be at slightly different distances can literally be a headache.',
})


bd3 = BM25F.exp.bag_dict().read(tokenizer, {
    '_id': '3',
    'title': 'd3',
    'body': 'The pace of the development of silicon photonics has quickened since 2004 due to investment by industry and government.',
})

bj.append(bd1)
bj.append(bd2)
bj.append(bd3)
'''

query = BM25F.exp.bag_of_words().read(tokenizer, 'Silicon Photonic')
print (query)
boost = BM25F.core.param_dict(default=1.0)
boost['title'] = 100
boost['abstract'] = 50
boost['body'] = 0.1

k1 = 2.0

b = BM25F.core.param_dict(default=0.75)
b['title'] = 0.75
b['abstract'] = 0.75
b['body'] = 0.75

scorer = BM25F.core.batch('_id', query, bj, boost, k1, b)
#print(scorer.top(4, [bd0, bd1, bd2, bd3]))
#print (type([bd0, bd1, bd2, bd3]))
#print (type(bj))
print(scorer.top(5, bj_list))