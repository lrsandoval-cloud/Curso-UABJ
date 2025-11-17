import pandas as pd

base = pd.read_pickle('pickles/base.pkl')

import spacy

nlp = spacy.load('es_core_news_sm')

base['lemas'] = ''

for i, row in base.iterrows():
    print(i, row['titulo'])
    if row['copete']:
        texto = row['copete']
        if texto[:-1] != '.':
            texto += '. '
        texto += row['texto']
    else:
        texto = row['texto']
    doc = nlp(texto)

    lemas = []
    for token in doc:
        if token.pos_ not in ['ADP', 'DET', 'PRON', 'NUM', 'CCONJ', 'SCONJ', 'PUNCT', 'SYM']:
            if not token.is_stop:
                lemas.append(token.lemma_.lower())
    base.loc[i, 'lemas'] = " ".join(lemas)


pd.to_pickle(base, 'pickles/base.pkl')
