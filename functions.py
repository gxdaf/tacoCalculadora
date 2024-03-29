from variables import *
import re

def loadTrs():
    '''
    Procura, salva e retorna todos as linhas da tabela externa para 
    consulta.
    '''
    table = driver.find_element_by_tag_name("table").get_attribute("outerHTML")
    soup = BeautifulSoup(table, 'html.parser')
    data = soup.find('tbody').find_all('tr')

    return data

def saveMarca(i):
    '''
    Salva a marca do alimento sendo visualizado caso ocorra a 
    diferenciação deste em função desta.
    '''
    #Carrega a tabela
    data = loadTrs()

    #Localiza a tupla do alimento
    tupla = data[i]

    #Localiza a célula correspondente à marca
    marca = tupla.find_all('td')[5].text

    return marca

def saveIds():
    '''
    Salva os IDs de todos os alimentos dispostos na página para o acesso.
    '''
    #Carrega todos as tuplas da tabela externa
    data = loadTrs()

    #Inicializa a lista vazia a ser populada com o id dos alimentos naquela página
    ids = []

    #Salva todos os Ids dos alimentos
    for d in data:
        i = d.find_all("td")[0].find("a")
        ids.append(i.text)

    return ids    

def saveTitle():
    '''
    Salva o nome de todos os alimentos na página para posterior registro 
    no banco junto a suas informações
    '''
    #Carrega todos as tuplas da tabela externa
    data = loadTrs()

    #Inicializa a lista vazia a ser populada com o nome dos alimentos naquela página
    titles = []

    #Salva todos os nomes dos alimentos
    for d in data:
        t = d.find_all("td")[1].find("a")
        titles.append(t.text)

    return titles

def clickId(id):
    '''
    Realiza o clique no ID do alimento a ser visualizado.
    '''
    #Clica no Id do alimento
    driver.find_element_by_link_text(id).click()
    
def loadTable():
    '''
    Carrega a tabela de informações da tabela do alimento sendo
    visualizado.
    '''
    #Carrega a tabela do alimento
    rows = driver.find_element_by_xpath("//*[@id='tabela1']").get_attribute("outerHTML")
    soup = BeautifulSoup(rows, 'html.parser')
    tr = soup.find('tbody').find_all('tr')

    return tr

def measuresNcompon():
    '''
    Salva as unidades e os componentes dos alimentos.
    '''
    #Carrega a tabela do alimento
    tabela = loadTable()
    
    #Salva todos as unidades de medida e componentes
    for celula in tabela:
        unid = celula.find_all('td')[1].get_text()
        comp = celula.find_all('td')[0].get_text()
        
        '''
        Confere se o componente já consta na lista 
        [True] Adiciona a unidade para complementar o nome.
        [False] Ignora.
        '''

        if componente.count(comp) > 0:
            comp += f' ({unid})'
        
        #Adiciona a unidade e o componente recuperados em seus dicionários
        unidade.append(unid)
        componente.append(comp)

    return unidade, componente

def checkForValues():
    '''
    Função que verifica se a tabela em questão está populada. Caso não esteja, 
    retorna false. O oposto retorna True.
    '''

    print("Procurando valores da tabela...")

    try:
        driver.find_element_by_xpath("//td[@class='dataTables_empty']")
        print("Tabela sem valores.")
        status_tabela = False #Seta o status padrão como False
    except:
        print("Dados encontrados.")
        status_tabela = True
    finally:
        return status_tabela

def saveInfoTr():
    '''
    Lê as informações (/100g) da tabela do alimento sendo visualizado e as 
    salva no dicionário sob índice homônimo, na mesma ordem das suas
    respectivas unidades de medida e componentes (fornecidos por esta,
    salvos na primeira iteração.)
    '''
    #Inicializa a lista que manterá os valores do alimento sendo visualizado a cada 100g.
    v = []
    
    #Carrega a tabela nutricional do alimento visualizado
    tabela = loadTable()

    #Alimenta o dicionário com os dados da tabela nutricional atual
    for celula in tabela:

        valor = celula.find_all('td')[2].get_text()
        
        if tabela.index(celula) not in [0,1]:
            if valor.find(',') != -1:
                valor = valor.replace(',', '.')
            elif re.search('[\w]+', valor) or re.search('[\W]+', valor):
                valor = '-1'
        
        print(f'{componente[tabela.index(celula)]}: {valor}')

        valor = float(valor)

        v.append(valor)
    
    return v

def evalNextPage():
    '''
    Avalia a existência de uma próxima página.
    '''
    prox = True

    print("Verificando a existência de uma próxima página...")
    try:
        nextPageBtn = driver.find_element_by_link_text("próxima »")
        print("Existe uma próxima página.")
    except:
        print("Esta é a última página.")
        prox = False
    else:
        nextPageBtn.click()
        print("Redirecionando para a próxima página...")
    finally:
        return prox

def getList(dict):
    '''
    Transforma os itens sob a chave 'Alimentos' em uma lista para iteração.
    '''
    list = []
    for key in dict.keys():
        if key != 'Unidades' and key != 'Componentes':
            list.append(key)

    return list

def insert(alimentos):
    '''
    Cria as instruções de inserção dos alimentos no banco de dados e as
    salva em um .txt para futura leitura e execução.
    '''

    #Inicializa o controlador de quantidade de iterações
    lc = len(alimentos['Componentes'])
    #Lista com o nome de todos os alimentos, para recuperação das informações no dicionário e inserção na tabela.
    alimento = getList(alimentos)
    la = len(alimento)

    #Inicialização das strings
    q = ""
    v = ""

    for y in range(la):
        #Alimento da vez
        a = alimento[y]

        for x in range(lc):
            dado = alimentos[a][x]

            if dado == -1:
                dado = None

            if x == 0:
                q = f"INSERT INTO alimentos(Nome, {alimentos['Componentes'][x]}, "
                v = f"('{a}', {dado}, "
            elif x == lc - 1:
                q += f"{alimentos['Componentes'][x]}) VALUES"
                v += f"{dado});"
            else:
                q += f"{alimentos['Componentes'][x]}, "
                v += f"{dado}, "

        #Monta a expressão de inserção
        ins = q + v

        with open("insercoes.txt", "a") as insert_file:
            linha = ins + "\n"
            print(linha)
            insert_file.write(linha)
