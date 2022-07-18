#!python3.8

import json

import numpy
from gensim.models import fasttext

model_path = "../wiki.ja/wiki.ja.bin"
model = fasttext.load_facebook_model(model_path)

##### test func #####
def test_calc_score(a, b):

    for i, j in b.items():
        b[i] = abs(j - a)

    return json.dumps(b, ensure_ascii=False)

def calc_score(plan_list: dict, word: str):
    
    similarities_dict = {plan : model.wv.similarity(plan, word).astype(numpy.unicode) for plan in plan_list.keys()}
    
    return json.dumps(similarities_dict, ensure_ascii=False)