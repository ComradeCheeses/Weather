"""

DO NOT RUN MANUALLY

THE PROGRAM WILL AUTOMATICALLY RUN THIS FILE

"""

import requests

def downloadimg(filename, url, data, ending):
    res = requests.get(f'{url}{data}{ending}')

    if res.status_code == 200:
        with open(filename, 'wb') as writer:
            writer.write(res.content)

def startup():
    started = open('data/setupmanager.txt', 'r').read()
    if started:
        return
    iconlist = ['01d', '02d', '03d', '04d', '09d', '10d', '11d', '13d', '50d']
    [downloadimg(f'data/assets/{i}.png', 'http://openweathermap.org/img/wn/', i, '@2x.png') for i in iconlist]
    with open('data/setupmanager.txt', 'w') as writer:
        writer.write('done')

if __name__ == '__main__':
    startup()


