# -*- coding: utf-8 -*-
import os
import sys
import time
import urllib3 #webdriver_manager
import json
import threading
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


urllib3.disable_warnings()
os.environ['WDM_LOG_LEVEL'] = '0'
os.environ['WDM_LOCAL'] = '0'
os.environ['WDM_SSL_VERIFY'] = '0'

#################################################################################


def now():
    formato="%d/%m/%Y %H:%M:%S"
    data_e_hora_atual = datetime.now()
    data_e_hora_formatada = data_e_hora_atual.strftime(formato)
    return data_e_hora_formatada


def driver_chrome(user_data):
    driver = None
    try:
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        #options.add_argument('--kiosk')
        #options.add_argument('--disable-dev-tools')
        #options.add_argument('—-disk-cache-size=0')
        #options.add_argument('--disable-application-cache')
        options.add_argument('--no-zygote')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--remote-debugging-port=0')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--mute-audio')
        options.add_argument('--disable-logging')        
        options.add_argument('--log-level=3')  # Configurar o nível de log para evitar mensagens específicas
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-default-driver-check')
        options.add_argument('--no-first-run')
        options.add_argument('--disable-xss-auditor')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-blink-features')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--ssl-insecure')
        options.add_argument('--window-size=1200,800')
        options.page_load_strategy = 'normal'
        options.add_argument('--user-data-dir='+ os.path.abspath(os.path.dirname(sys.argv[0])) + '\\user-data\\' + user_data)
        options.add_experimental_option('excludeSwitches', ['enable-logging','enable-automation',"ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection",])
        options.add_experimental_option('useAutomationExtension', False)
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)
        executable_path = ChromeDriverManager().install()
        service = ChromeService(executable_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_window_size(1200, 800)
        driver.set_page_load_timeout(10)
        driver.implicitly_wait(10)
        driver.set_script_timeout(10)
    except Exception as e:
        print(e)
    return driver

def folhacerta(nome, email, password):
    print(nome, ',Abrindo Google Chrome')
    browser = driver_chrome(nome)
    browser.get('https://portal.folhacerta.com/login/')
    time.sleep(1)
    #print(browser.current_url)
    if browser.current_url == 'https://portal.folhacerta.com/login/':   
        try:
            # Aguarda até que o campo de e-mail esteja presente na página
            email_field = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            # Digita o e-mail no campo
            email_field.send_keys(email + Keys.RETURN)
            time.sleep(1)

            password_field = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            # Digita o password no campo
            password_field.send_keys(password + Keys.RETURN)
            time.sleep(1)
        except:
            pass
        try:
            browser.find_element(By.ID, "rcc-confirm-button").click() #aceitar_button
            time.sleep(1)
        except:
            pass

    try:
        marcar_ponto_button = browser.find_element(By.XPATH, "/html/body/div/div[2]/div/div[3]/div[2]/div/div[3]/button/label[2]")
        marcar_ponto_button.click()
        time.sleep(1)
        confirmar_button = browser.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div/div/div[2]/button[2]")
        # confirmar_button.click()
        print(nome, 'Marcou o Ponto:', now())
        
    except:
        pass

    #x = input('Pause...')
    browser.quit()
    print(nome, ',Finalizado.')

#################################################################################
# 1
#folhacerta('yuri', 'yliranunes@gmail.com', '1234')
#sys.exit()

# Lê o arquivo JSON
with open('config.json', 'r') as arquivo:
    usuarios = json.load(arquivo)
# 2
#for usuario in usuarios:
#    folhacerta(usuario['nome'], usuario['email'], usuario['password'])

# 3
# Lista para armazenar as threads
threads = []

# Loop para criar e iniciar as threads
for usuario in usuarios:
    args = (usuario['nome'], usuario['email'], usuario['password'])
    thread = threading.Thread(target=folhacerta, args=args)
    threads.append(thread)
    thread.start()

# Aguarda todas as threads terminarem
for thread in threads:
    thread.join()
