import pandas as pd

base = pd.read_pickle('pickles/base.pkl')

print('Ingrese los índices de los registros a eliminar, separados por coma')
elimina = input()
print()

ids = elimina.split(',')

for id in ids:
    try:
        if base.loc[int(id), 'titulo'] != '':
            print('¿Eliminar el artículo "' + base.loc[int(id), 'titulo'] + '" de la base? (si/no)')
        else:
            print('¿Eliminar el registro', id, '? (si/no)')
    except TypeError:
        print('¿Eliminar el registro', id, '? (si/no)')
    respuesta = input()
    if respuesta == 'si':
        base.drop([int(id)], axis=0, inplace=True)
        print('Registro eliminado')
    else:
        print('No se modificó la base de datos')
    print()

base.reset_index(drop=True, inplace=True)
pd.to_pickle(base, 'pickles/base.pkl')
