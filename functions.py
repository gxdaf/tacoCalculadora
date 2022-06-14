from variables import *
import re

def loadTrs():
    '''
    Procura, salva e retorna todos as linhas da tabela externa para consulta.
    '''
    table = driver.find_element_by_tag_name("table").get_attribute("outerHTML")
    soup = BeautifulSoup(table, 'html.parser')
    data = soup.find('tbody').find_all('tr')

    return data

def saveMarca(i):
    data = loadTrs()

    celula = data[i]

    marca = celula.find_all('td')[5].text

    print(marca)

    return marca

def saveIds():

    #Carrega todos as tuplas da tabela externa
    data = loadTrs()

    #Inicializa a lista vazia a ser populada com o id dos alimentos naquela página
    ids = []

    #Salva todos os Ids dos alimentos
    for d in data:
        i = d.find_all("td")[0].find("a")
        ids.append(i.text)

    print(ids)

    return ids    

def saveTitle():
    #Carrega todos as tuplas da tabela externa
    data = loadTrs()

    #Inicializa a lista vazia a ser populada com o nome dos alimentos naquela página
    titles = []

    #Salva todos os nomes dos alimentos
    for d in data:
        t = d.find_all("td")[1].find("a")
        titles.append(t.text)

    print(titles)

    return titles

def clickId(id):
    #Clica no Id do alimento
    driver.find_element_by_link_text(id).click()
    
def loadTable():
    #Carrega a tabela do alimento
    rows = driver.find_element_by_xpath("//*[@id='tabela1']").get_attribute("outerHTML")
    soup = BeautifulSoup(rows, 'html.parser')
    tr = soup.find('tbody').find_all('tr')

    return tr

def measuresNcompon():
    #Carrega a tabela do alimento
    tabela = loadTable()
    
    #Salva todos as unidades de medida e componentes
    for celula in tabela:
        unidade.append(celula.find_all('td')[1].get_text())
        componente.append(celula.find_all('td')[0].get_text())

    return unidade, componente

def saveInfoTr():
    #Inicializa a lista que manterá os valores do alimento sendo visualizado a cada 100g.
    v = []
    
    #Carrega a tabela nutricional do alimento visualizado
    tabela = loadTable()

    #Alimenta o dicionário com os dados da tabela nutricional atual
    for celula in tabela:

        valor = celula.find_all('td')[2].get_text()
        
        if valor.find(',') != -1:
            valor = valor.replace(',', '.')
        elif re.search('[\w]+', valor) or re.search('[\W]+', valor):
            valor = '-1'
        
        valor = float(valor)

        v.append(valor)
    
    return v

def evalNextPage():
    nextPageBtn = driver.find_element_by_link_text("próxima »")
    
    if nextPageBtn.is_displayed():
        nextPageBtn.click()
    else:
        prox = False
        for k, v in alimentos.items():
            print(f'{k}: {v}')