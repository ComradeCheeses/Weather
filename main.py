import pygame, requests
from setup import startup
import settings
from datetime import datetime
import os
from pygame._sdl2 import Window
import pyautogui as pg
from email.message import EmailMessage
import ssl, smtplib

# NOTE    REMOVE FREEZING CODE BEFORE UPLOADING



def download_img(url, file_name, data, ending):
    res = requests.get(f'{url}{data}{ending}')
    if res.status_code == 200:
        with open(file_name, 'wb') as writer:
            writer.write(res.content)

class Weather():
    def __init__(self):

        pygame.init()
        startup()

        self.font = pygame.font.SysFont('Ebrima.ttf', 20)

        self.display = pygame.display.set_mode((250, 100), pygame.NOFRAME)
        self.pgwindow = Window.from_display_module() 
        self.pgwindow.position = (500, 500)
        self.clock = pygame.time.Clock()

        download_img('http://openweathermap.org/img/wn/','data/assets/icon.png' , '02d', '@2x.png')

        self.key = '6e73b045f4e2300d93977250549bdb9a'

        self.weatherdata = self.getweatherdata(settings.CITY)
        print(self.weatherdata)
    
    def getweatherdata(self, city):
        return requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&APPID={self.key}').json()
    
    def geticontag(self):
        if self.weatherdata['weather'][0]['main'] == 'Thunderstorm':
            return '11d'
        elif self.weatherdata['weather'][0]['main'] == 'Drizzle':
            return '09d'
        elif self.weatherdata['weather'][0]['main'] == 'Snow':
            return '13d'
        elif self.weatherdata['weather'][0]['main'] in ['Mist', 'Smoke', 'Haze', 'Dust', 'Fog', 'Sand', 'Ash', 'Squall', 'Tornado']:
            return '50d'
        elif self.weatherdata['weather'][0]['main'] == 'Clouds':
            if self.weatherdata['weather'][0]['description'] == 'few clouds':
                return '02d'
            elif self.weatherdata['weather'][0]['description'] == 'scattered clouds':
                return '03d'
            elif self.weatherdata['weather'][0]['description'] == 'broken clouds' or self.weatherdata['weather'][0]['description'] == 'overcast clouds':
                return '04d'
        elif self.weatherdata['weather'][0]['main'] == 'Clear':
            return '01d'
        else:
            exit()
    
    def main(self):
        moving = False
        freezing = False
        sent = False
        while True:
            self.clock.tick(60)
            self.display.fill((255, 255, 255))
            now = datetime.now()
            if now.second == 0:
                self.weatherdata = self.getweatherdata(settings.CITY)
                if (self.weatherdata['main']['temp']-273.15)*(9/5)+32 <= 31:
                    freezing = True
                else:
                    freezing = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_pos = pg.position()
                    self.win_position = self.pgwindow.position
                    moving = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    moving = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

            if freezing:
                pygame.draw.polygon(self.display, (255, 0, 0), ((3, 98), (21, 98), (12, 80)))
                self.display.blit(self.font.render('Freezing Temperatures', True, (0, 0, 0), (255, 255, 255)), (23, 84))

            if moving:
                self.pgwindow.position = (self.win_position[0]+(pg.position()[0]-self.mouse_pos[0]), self.win_position[1]+(pg.position()[1]-self.mouse_pos[1]))

            icon = pygame.image.load(f'{os.path.dirname(__file__)}\\data\\assets\\{self.geticontag()}.png')
            self.display.blit(icon, (-20, -20))
            temp = (self.weatherdata['main']['temp']-273.15)*(9/5)+32
            humidity = self.weatherdata['main']['humidity']
            self.display.blit(self.font.render(f'Temp: {round(temp, 1)}*F  Humidity: {humidity}', True, (0, 0, 0), (255, 255, 255)), (75, 10))
            pygame.display.update()



weather = Weather()
weather.main()


