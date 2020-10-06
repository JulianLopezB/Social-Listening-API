import requests
import json

# EJEMPLO SENTIMENT Y TAGS

ejemplo = ['Me podrian pasar mas info por favor?']
parametros = {'text': ejemplo}


# Predice sentiment y tags
r = requests.get('http://localhost:5000/predict',params=parametros)


print('\n')
print('\n')
print(f'texto: {ejemplo}')

print('************************  SENTIMENT/TAGS ****************************')

print('\n')
print('output: \n')
print('\n'.join('{}: {}'.format(*k) for k in r.json().items()))
print('\n')


r = requests.get('http://localhost:5000/audiencias',params=parametros)


print('\n')
print('************************  AUDIENCIAS ****************************')

print('\n')
print('output: \n')
print('\n'.join('{}: {}'.format(*k) for k in r.json().items()))
print('\n')
