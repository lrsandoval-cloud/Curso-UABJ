muestra = 50        # Indicar el número de casos que incluirá la muestra
salida_txt = True   # Indicar True si se quiere que genere un archivo 'cuotas.txt' en lugar de mostrar en pantalla

import pandas as pd

base = pd.read_pickle('pickles/base.pkl')

rotulos = list(base['medio'].unique())
clusters = len(list(base['cluster'].unique()))

cantidades = {}
porcentuales = {}
n_cuotas = {}
cuotas = {}
for medio in rotulos:
    notas = []
    porcientos = []
    cuota = []
    n_cuota = []
    for c in range(clusters):
        notas.append(len(base.query('medio == "' + medio + '" and cluster == ' + str(c))))
        porcientos.append(len(base.query('medio == "' + medio + '" and cluster == ' + str(c))) / len(base) * 100)
        celda = round(len(base.query('medio == "' + medio + '" and cluster == ' + str(c))) / len(base) * muestra)
        seleccion = base.query('medio == "' + medio + '" and cluster == ' + str(c)).sort_values('distancia')[:celda].copy()
        cuota.append(seleccion.index.tolist())
        n_cuota.append(celda)

    cantidades[medio] = notas
    porcentuales[medio] = porcientos
    n_cuotas[medio] = n_cuota
    cuotas[medio] = cuota

k_notas = pd.DataFrame(cantidades).transpose()
k_porcentajes = pd.DataFrame(porcentuales).transpose()
k_cuotas = pd.DataFrame(cuotas).transpose()
k_n_cuotas = pd.DataFrame(n_cuotas).transpose()

if salida_txt == False:
    print('DISTRIBUCIÓN DE NOTAS POR MEDIO Y CLÚSTER')
    print(k_notas, end='\n\n')
    print('PORCENTAJES DE NOTAS POR MEDIO Y CLÚSTER')
    print(k_porcentajes, end='\n\n')
    print('IDs DE LOS ARTÍCULOS SELECCIONADOS PARA LA MUESTRA')
    print(k_cuotas, end='\n\n')
    print('CUOTAS POR MEDIO Y CLÚSTER')
    print(k_n_cuotas)
else:
    cuotas = 'DISTRIBUCIÓN DE NOTAS POR MEDIO Y CLÚSTER\n'
    cuotas += k_notas.to_string()
    cuotas += '\n\nPORCENTAJES DE NOTAS POR MEDIO Y CLÚSTER\n'
    cuotas += k_porcentajes.to_string()
    cuotas += '\n\nIDs DE LOS ARTÍCULOS SELECCIONADOS PARA LA MUESTRA\n'
    cuotas += k_cuotas.to_string()
    cuotas += '\n\nCUOTAS POR MEDIO Y CLÚSTER\n'
    cuotas += k_n_cuotas.to_string()
    archivo_cuotas = open('cuotas.txt', 'w')
    archivo_cuotas.write(cuotas)
    archivo_cuotas.close()


texto = '<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="UTF-8">\n</head>\n<body>\n'

for i, row in k_cuotas.iterrows():
    texto += '<h3>' + i + '</h3>'
    for c in range(clusters):
        for nota in row[c]:
            texto += '<p><a href="' + base.loc[nota, 'url'] + '">' + base.loc[nota, 'titulo'] + '</a> (' + str(c) + ')</p>\n'

texto + "</body>\n</html>"

archivo_muestra = open('muestra.html', 'w')
archivo_muestra.write(texto)
archivo_muestra.close()




