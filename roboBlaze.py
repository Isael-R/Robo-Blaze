from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
import requests
import json


service = Service(ChromeDriverManager().install())
drive = webdriver.Chrome(service=service)

# Requisição site Blaze
drive.get('https://blaze.com/pt/games/double?modal=auth&tab=login')

#Aréa Login e redirecionamento para Double
sleep(1)
drive.find_element(By.XPATH, '//*[@id="auth-modal"]/div[2]/form/div[1]/div/input').send_keys('Gmail')
sleep(1)
drive.find_element(By.XPATH, '//*[@id="auth-modal"]/div[2]/form/div[2]/div/input').send_keys('Senha')
sleep(2)
drive.find_element(By.XPATH, '//*[@id="auth-modal"]/div[2]/form/div[4]/button').click()
sleep(6)

#Valor da Entrada
sleep(5)
drive.find_element(By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[2]/div[1]/div/div[1]/input').send_keys('1')
sleep(5)

#Aréa da Estrageia e Envio da Aposta
ultimos_20giros = []
cor_vermelha = []
cor_preta = []
ultimos_2giros = []
aposta = ''

while True:
    # Roleta girando ou não
    time_roleta = drive.find_element(By.CLASS_NAME, 'time-left').text
    roleta = time_roleta[:10].strip()
    if roleta in 'Girando Em':
        while True:
            request_api = requests.get('https://blaze.com/api/roulette_games/recent')
            response = request_api.json()

            #Pegando apenas os ultimos 20 giros da roleta
            for resultado in response:
                ultimos_20giros.append( resultado["color"])
            #Separado a quantidas de cores pretas e vermelhas
            for giro in ultimos_20giros:
                if giro == 1:
                    cor_vermelha.append(giro)
                elif giro == 2:
                    cor_preta.append(giro)
            #Pegando apenas os ultimos 2 giros anteriores da roleta
            ultimos_2giros.append(ultimos_20giros[:2])
            #Estrategia    
            if len(cor_preta) > len(cor_vermelha):
                if ultimos_2giros[0][0] == 2 and ultimos_2giros[0][1] == 2:
                    aposta = "preta"
            else:
                if ultimos_2giros[0][0] == 1 and ultimos_2giros[0][1] == 1 :
                    aposta = 'vermelha'

            if aposta :
                if aposta in 'vermelha':
                    drive.find_element(By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[2]/div[2]/div/div[1]').click()
                    drive.find_element(By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[3]/button').click()
                    sleep(45)
                else:
                    drive.find_element(By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[2]/div[2]/div/div[3]/div').click()
                    drive.find_element(By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[3]/button').click()
                    sleep(45)       
            break
    else:
            sleep(2)
    aposta = ''
    ultimos_20giros.clear()
    cor_preta.clear()
    cor_vermelha.clear()
    ultimos_2giros.clear()
