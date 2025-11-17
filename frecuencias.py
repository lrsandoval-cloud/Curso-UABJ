keyword = 'padre'

import pandas as pd
from funciones import obtener_dic_palabras

base = pd.read_pickle('pickles/base.pkl')
rotulos = list(base['medio'].unique())

palabras = obtener_dic_palabras(base)

from nltk.text import Text

frecuencias = []

for medio, pal in palabras.items():
    tokens = pal.split(" ")

    texto_nltk = Text(tokens)
    valor = texto_nltk.count(keyword) / len(tokens) * 100
    frecuencias.append(valor)


import matplotlib.pyplot as plt

fig, ax = plt.subplots()
barras = ax.bar(rotulos, frecuencias)
ax.bar_label(barras)
plt.title("Frecuencia de uso del término: " + keyword + "\n")
plt.show()
