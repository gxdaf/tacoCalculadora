from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox import firefox_profile, options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import select
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

'''
Definições Selenium
'''
option = Options()
#option.headless = True
driver = webdriver.Firefox(options=option)
url = "http://www.tbca.net.br/base-dados/composicao_alimentos.php"

'''
Definições built-in
'''
#Inicializa as listas de unidades de medida e componentes
unidade, componente = [], []