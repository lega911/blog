
cmap0 = 'йцукенгшщзхъэждлорпавыфячсмитьбю'
cmap1 = 'icukengsszh_egdlorpavifihsmit_bu'

cmap = {}
for a, b in zip(cmap0, cmap1):
    cmap[a] = b


def encode(s):
    r = []
    for a in s.lower():
        if a in '0123456789qwertyuiopasdfghjklzxcvbnm_':
            r.append(a)
        if a in cmap:
            r.append(cmap[a])
    result = ''.join(r)
    assert result, s
    return result
