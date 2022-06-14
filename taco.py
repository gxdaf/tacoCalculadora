from  functions import *
from variables import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox import firefox_profile, options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import select
from selenium.webdriver.support.select import Select
from dicexpec import c
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from dbsql import cr_tab, drop_tab, ins_tab

#Dicionário de armazenamento das informações a serem enviadas ao banco
alimentos = {}

driver.get(url)

def collect(alimentos):
    c = 0

    while prox:
        a = {}
        
        #Salva os nomes dos alimentos da página atual
        titulos = saveTitle()

        #Salva os Ids dos alimentos da página atual
        ids = saveIds()
        
        for i in range(len(ids)):

            #Atribui o nome do alimento sendo visualizado como seu título
            titulo = titulos[i]

            '''
            Verifica se o alimento em questão já não consta na lista.
            [True] Trata-se da avaliação de diferentes marcas. Nesse caso, é salvo o nome desta.
            [False] Nada ocorre.
            '''
            if titulos.count(titulo) > 1:
                marca = saveMarca(i)
                titulo += f' ({marca})'
            
            print(titulo)

            #Clica no alimento
            clickId(ids[i])
            
            '''
            Verifica se é a primeira iteração.
            [True] Salva as unidades de medida e os componentes em suas respectivas chaves.
            [False] Ignora e somente salva os alimentos e seus valores em 100g.
            ''' 
            if c == 0:
                u, c = measuresNcompon()
                alimentos.update({'Unidades': u, 'Componentes':c})

            #Informações nutricionais do alimento sendo visualizado
            nutricInfo = saveInfoTr()

            #Salva o alimento (nome e informações) no dicionário
            alimentos.update({titulo: nutricInfo})

            #print(alimentos)

            driver.back()
        
        #Adiciona 1 ao contador de iterações
        c += 1
        
        '''
        Avalia se há uma próxima página a ser clicada.
        [True] Vai para a próxima página.
        [False] Inicia o envio de informações ao banco.
        '''

        evalNextPage()
    
collect(alimentos)