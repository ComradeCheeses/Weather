import requests, pprint

key = '6e73b045f4e2300d93977250549bdb9a'
city = 'Katy'

data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}').json()

pprint.pprint(data)
