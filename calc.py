#!python3.8

import json

##### test func #####
def test_calc_score(a, b):
    for i, j in b.items():
        b[i] = abs(j - a)

    return json.dumps(b, ensure_ascii=False)
