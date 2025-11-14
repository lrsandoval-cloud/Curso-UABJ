import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean

base = pd.read_pickle('pickles/base.pkl')
rotulos = list(base['medio'].unique())

base['largo'] = base['texto'].str.len()
largos_promedio = []

for rotulo in rotulos:
    segmento = base.query("medio == '" + rotulo + "'")
    promedio = int(mean(segmento['largo']))
    largos_promedio.append(promedio)

fig, ax = plt.subplots()
barras = ax.bar(rotulos, largos_promedio)
ax.bar_label(barras)
plt.title("Cantidad de caracteres promedio por nota")
plt.show()