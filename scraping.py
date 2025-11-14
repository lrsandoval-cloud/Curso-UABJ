from bs4 import BeautifulSoup
import requests
import funciones
import pandas as pd
import time

sitio = 'lanacion'

d_titulo = {
    'tag' : 'h1',
    'attrs' : {'class': 'com-title'}
}

d_copete = {
    'tag' : 'h2',
    'attrs' : {'class': 'com-subhead'}
}

d_texto = {
    'tag' : ['h2', 'p'],
    'attrs' : {'class' : ['com-paragraph', 'com-title']}
}

d_fecha = {
    'tag': 'time',
    'attrs' : {'class': 'com-date'}
}

df = pd.DataFrame(columns = ['medio', 'titulo', 'fecha', 'copete', 'texto', 'url', 'ranking'])

direcciones = open('listados/' + sitio + '.txt', 'r')
ranking = 1
for l in direcciones:
    url = l[:-1]
    print(ranking, url)
    pagina = requests.get(url)
    sopa = BeautifulSoup(pagina.text, 'lxml')
    cuerpo = sopa.find('body')

    titulo = ''
    titulo1 = cuerpo.find(d_titulo['tag'], d_titulo.get('attrs', {}))
    if titulo1:
        try:
            titulo = titulo1.text
        except AttributeError:
            titulo = ''

    texto = ''
    parrafos = cuerpo.find_all(d_texto['tag'], d_texto.get('attrs', {}))
    if parrafos:
        for p in parrafos:
            texto += p.text + ' '

    copete = ''
    parrafos = cuerpo.find(d_copete['tag'], d_copete.get('attrs', {}))
    if parrafos:
        for p in parrafos:
            copete += p.text + ' '

    fecha = ''
    fecha1 = cuerpo.find(d_fecha['tag'], d_fecha.get('attrs', {}))
    if fecha1:
        try:
            fecha = funciones.formato_fecha(fecha1.text)
        except AttributeError:
            fecha = ''

    '''
    print(titulo)
    print(copete)
    print(texto)
    print(fecha)
    exit()
    '''

    df.loc[len(df)] = {
        'medio' : sitio,
        'titulo' : titulo,
        'fecha' : fecha,
        'copete' : copete,
        'texto' : texto,
        'url' : url,
        'ranking' : ranking
    }

    ranking += 1
    time.sleep(1)
    if ranking % 10 == 0:
        df.to_pickle('pickles/' + sitio + '.pkl')

df.to_pickle('pickles/' + sitio + '.pkl')

print(df)