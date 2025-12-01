import pandas as pd
from funciones import obtener_dic_palabras
from funciones import obtener_stop_words
from statistics import mean
import matplotlib.pyplot as plt

base = pd.read_pickle('pickles/base.pkl')

rotulos = list(base['medio'].unique())
clusters = list(base['cluster'].unique())

palabras = obtener_dic_palabras(base)

stop_words = obtener_stop_words()

sentimientos = pd.read_pickle('pickles/sentimientos.pkl')

sentimientos['label'] = sentimientos['label'].astype(int)
for i, row in sentimientos.iterrows():
    if row['fecha'] == '0000-00-00':
        sentimientos.loc[i, 'fecha'] = '2024-01-01'


base['label'] = 0.0

for i, row in base.iterrows():
    parte = sentimientos.query("idnota == " + str(i))
    media = mean(parte['label'])
    base.loc[i, 'label'] = media
    if row['fecha'] == '0000-00-00':
        base.loc[i, 'fecha'] = '2024-01-01'

sentires = base.groupby("cluster")["label"].mean().tolist()

fig, ax = plt.subplots()
barras = ax.bar(clusters, sentires)
ax.bar_label(barras)
plt.title("Análisis de sentimiento: label promedio por cluster")
plt.show()

base['fecha'] = pd.to_datetime(base['fecha'])
base['mes'] = base['fecha'].dt.to_period('M')   # formato YYYY-MM
prom = base.groupby(['mes', 'cluster'])['label'].mean().reset_index()
pivot = prom.pivot(index='mes', columns='cluster', values='label')

plt.figure(figsize=(10,6))

for cluster in pivot.columns:
    plt.plot(pivot.index.astype(str), pivot[cluster], marker='o', label=cluster)

plt.xlabel('Mes')
plt.ylabel('Promedio de sentimiento')
plt.title('Sentimiento promedio mensual por clúster')
plt.xticks(rotation=45)
plt.legend(title='Clúster')
plt.tight_layout()
plt.show()
