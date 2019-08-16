#PROJETO 2 - 2048

#81186 - Stephane Duarte
#81858 - Joao Oliveira


#importa a funcao random
import random

#TAD COORDENADA

def cria_coordenada(l,c):
    #recebe dois inteiros e devolve uma coordenada(tuplo)
    """A funcao verifica se os argumentos sao validos e cria a coordenada correspondente."""
    if l < 1 or c < 1 or l > 4 or c > 4 or not isinstance(l,int) or not isinstance(c,int):
        raise ValueError('cria_coordenada: argumentos invalidos')
    else:
        return (l,c)
    
def coordenada_linha(coord):
    """A funcao devolve a linha da coordenada."""
    return coord[0]

def coordenada_coluna(coord):
    """A funcao devolve a coluna da coordenada."""
    return coord[1]

def e_coordenada(coord):
    """A funcao verifica se o argumento corresponde a uma coordenada valida."""
    return (isinstance(coord,tuple) and len(coord) == 2 and\
            coord[0] > 0 and coord[0] <= 4 and isinstance(coord[0],int) and\
            coord[1] > 0 and coord[1] <= 4 and isinstance(coord[1],int))

def coordenadas_iguais(coord1,coord2):
    """A funcao verifica se os argumentos sao iguais."""
    return (coordenada_linha(coord1) == coordenada_linha(coord2) and \
            coordenada_coluna(coord1) == coordenada_coluna(coord2))
    
#TAD TABULEIRO:

def cria_tabuleiro():
    """A funcao cria um tabuleiro."""
    return [[0,0,0,0],\
            [0,0,0,0],\
            [0,0,0,0],\
            [0,0,0,0],\
            0]

def tabuleiro_posicao(tab,coord):
    """A funcao devolve o valor correspondente a coordenada inserida, se esta for valida."""
    if not e_coordenada(coord):
        raise ValueError('tabuleiro_posicao: argumentos invalidos') 
    else:
        for l in range(1,5):
            for c in range(1,5):
                C = cria_coordenada(l,c)
                if coordenadas_iguais(C,coord):
                    return tab[coordenada_linha(coord)-1][coordenada_coluna(coord)-1]
    
def tabuleiro_pontuacao(tab):
    """A funcao devolve a pontuacao do tabuleiro."""
    return tab[4]
        
def tabuleiro_posicoes_vazias(tab):
    """A funcao devolve uma lista com todas as coordenadas das posicoes vazias do tabuleiro."""
    vazio = []
    for i in range(1,5):
        for j in range(1,5):
            C = cria_coordenada(i,j)
            valor = tabuleiro_posicao(tab,C)
            if valor == 0:
                vazio = vazio + [C]
    return vazio

def tabuleiro_preenche_posicao(tab,coord,val):
    """A funcao preenche a coordenada referenciada com o valor inserido."""
    if not isinstance(val,int) or not e_coordenada(coord):
        raise ValueError('tabuleiro_preenche_posicao: argumentos invalidos')
    else:
        for l in range(1,5):
            for c in range(1,5):
                C = cria_coordenada(l,c)
                if coordenadas_iguais(C,coord):
                    tab[coordenada_linha(C)-1][coordenada_coluna(C)-1] = val
    return tab

def tabuleiro_actualiza_pontuacao(tab,val):
    """A funcao atualiza o valor da pontuacao do tabuleiro, somando-lhe o valor inserido."""
    if not isinstance(val,int) or val < 0 or val % 4 != 0:
        raise ValueError('tabuleiro_actualiza_pontuacao: argumentos invalidos')
    else:
        tab[4] = tabuleiro_pontuacao(tab) + val
    return tab

def muda_posicao(tab,ccar):
    """A funcao muda as posicoes dos valores do tabuleiro, consoante a orientacao selecionada."""
    #a funcao verifica se a posicao seguinte a uma determinada coordenada tem valor 0.
    #se tiver valor 0, modifica todos os valores de acordo com a direcao pretendida.
    for l in range(1,5):
            for c in range(1,5):
                coordirecao = (('N', (l+1,c), (l+2,c), (l+3,c)),
                               ('S', (l-1,c), (l-2,c), (l-3,c)),
                               ('W', (l,c+1), (l,c+2), (l,c+3)),
                               ('E', (l,c-1), (l,c-2), (l,c-3)))
                coord0 = 0
                coord1 = 0
                coord2 = 0
                coord3 = 0
                for direcao in coordirecao:
                    if ccar in direcao[0]:
                        coord0 = cria_coordenada(l,c)
                        if direcao[1][0] > 0 and direcao[1][0] < 5 and direcao[1][1] > 0 and direcao[1][1] < 5:
                            coord1 = cria_coordenada(direcao[1][0],direcao[1][1])
                        if direcao[2][0] > 0 and direcao[2][0] < 5 and direcao[2][1] > 0 and direcao[2][1] < 5:
                            coord2 = cria_coordenada(direcao[2][0],direcao[2][1])
                        if direcao[3][0] > 0 and direcao[3][0] < 5 and direcao[3][1] > 0 and direcao[3][1] < 5:
                            coord3 = cria_coordenada(direcao[3][0],direcao[3][1])
                        valorC0 = tabuleiro_posicao(tab,coord0)
                        if valorC0 == 0:
                            if e_coordenada(coord1):
                                valorC1 = tabuleiro_posicao(tab,coord1)
                                valorC0 = valorC1
                                valorC1 = 0
                                tabuleiro_preenche_posicao(tab,coord0,valorC0)
                                tabuleiro_preenche_posicao(tab,coord1,valorC1)
                                if e_coordenada(coord2):
                                    valorC2 = tabuleiro_posicao(tab,coord2)
                                    valorC1 = valorC2
                                    valorC2 = 0
                                    tabuleiro_preenche_posicao(tab,coord1,valorC1)
                                    tabuleiro_preenche_posicao(tab,coord2,valorC2)
                                    if e_coordenada(coord3):
                                        valorC3 = tabuleiro_posicao(tab,coord3)
                                        valorC2 = valorC3
                                        valorC3 = 0
                                        tabuleiro_preenche_posicao(tab,coord2,valorC2)
                                        tabuleiro_preenche_posicao(tab,coord3,valorC3)
                                        coord0 = 0                                
    return tab

def soma_numeros(tab,ccar):
    """A funcao soma os valores do tabuleiro consoante a orientacao escolhida."""
    #a funcao soma os valores de duas coordenadas se os seus valores forem iguais e as coordenadas tiverem na direcao pretendida.
    i = 1
    for c in range(1,5):
        coordsoma = (('N', cria_coordenada(i,c), cria_coordenada(i+1,c), cria_coordenada(i+2,c), cria_coordenada(i+3,c)),
                     ('S', cria_coordenada(i+3,c), cria_coordenada(i+2,c), cria_coordenada(i+1,c), cria_coordenada(i,c)),
                     ('W', cria_coordenada(c,i), cria_coordenada(c,i+1), cria_coordenada(c,i+2), cria_coordenada(c,i+3)),
                     ('E', cria_coordenada(c,i+3), cria_coordenada(c,i+2), cria_coordenada(c,i+1), cria_coordenada(c,i)))
        for direc in coordsoma:
            if ccar in direc[0]:
                coord1 = direc[1]
                coord2 = direc[2]
                coord3 = direc[3]
                coord4 = direc[4]
                valorC1 = tabuleiro_posicao(tab,coord1)
                valorC2 = tabuleiro_posicao(tab,coord2)
                valorC3 = tabuleiro_posicao(tab,coord3)
                valorC4 = tabuleiro_posicao(tab,coord4)
                if e_coordenada(coord1) and e_coordenada(coord2):
                    if valorC1 == valorC2:
                        valorC1 = valorC1 + valorC2
                        tabuleiro_actualiza_pontuacao(tab,valorC1)
                        valorC2 = 0
                if e_coordenada(coord2) and e_coordenada(coord3):
                    if valorC2 == valorC3:
                        valorC2 = valorC2 + valorC3
                        tabuleiro_actualiza_pontuacao(tab,valorC2)
                        valorC3 = 0
                if e_coordenada(coord3) and e_coordenada(coord4):
                    if valorC3 == valorC4:
                        valorC3 = valorC3 + valorC4
                        tabuleiro_actualiza_pontuacao(tab,valorC3)
                        valorC4 = 0
                tabuleiro_preenche_posicao(tab,coord1,valorC1)
                tabuleiro_preenche_posicao(tab,coord2,valorC2)
                tabuleiro_preenche_posicao(tab,coord3,valorC3)
                tabuleiro_preenche_posicao(tab,coord4,valorC4)             
    return tab
    
def tabuleiro_reduz(tab,ccar):
    """A funcao reduz o tabuleiro consoante a orientacao escolhida."""
    copiatab = []
    while tab != copiatab:
        copiatab = copia_tabuleiro(tab)        
        muda_posicao(tab,ccar)
    soma_numeros(tab,ccar)
    muda_posicao(tab,ccar)
    return tab
                        
def e_tabuleiro(tab):
    """A funcao verifica se o argumento e um tabuleiro valido."""
    return (isinstance(tab,list) and len(tab) == 5)

def tabuleiro_terminado(tab):
    """A funcao verifica se o tabuleiro esta concluido, nao existindo mais opcoes de jogo."""
    vazio = tabuleiro_posicoes_vazias(tab)
    copitab1 = copia_tabuleiro(tab)
    copitab2 = copia_tabuleiro(tab)
    copitab3 = copia_tabuleiro(tab)
    copitab4 = copia_tabuleiro(tab)
    return (vazio == [] and tabuleiro_reduz(tab, 'N') == copitab1 and tabuleiro_reduz(tab, 'S') == copitab2 \
            and tabuleiro_reduz(tab, 'E') == copitab3 and tabuleiro_reduz(tab, 'W') == copitab4)

def tabuleiros_iguais(tab1,tab2):
    """A funcao verifica se os dois tabuleiros recebidos como argumentos sao iguais."""
    coordiguais = 0
    for l in range(1,5):
        for c in range(1,5):
            if tab1[l-1][c-1] == tab2[l-1][c-1]:
                coordiguais = coordiguais + 1
    if tab1[4]==tab2[4]:
        coordiguais = coordiguais + 1
    return(coordiguais == 17)

def escreve_tabuleiro(tab):
    """A funcao escreve o tabuleiro na forma classica do jogo."""
    if e_tabuleiro(tab):
        print('[',tabuleiro_posicao(tab,cria_coordenada(1,1)),'] [',tabuleiro_posicao(tab,cria_coordenada(1,2)),'] [',tabuleiro_posicao(tab,cria_coordenada(1,3)),'] [',tabuleiro_posicao(tab,cria_coordenada(1,4)),'] ')
        print('[',tabuleiro_posicao(tab,cria_coordenada(2,1)),'] [',tabuleiro_posicao(tab,cria_coordenada(2,2)),'] [',tabuleiro_posicao(tab,cria_coordenada(2,3)),'] [',tabuleiro_posicao(tab,cria_coordenada(2,4)),'] ')
        print('[',tabuleiro_posicao(tab,cria_coordenada(3,1)),'] [',tabuleiro_posicao(tab,cria_coordenada(3,2)),'] [',tabuleiro_posicao(tab,cria_coordenada(3,3)),'] [',tabuleiro_posicao(tab,cria_coordenada(3,4)),'] ')
        print('[',tabuleiro_posicao(tab,cria_coordenada(4,1)),'] [',tabuleiro_posicao(tab,cria_coordenada(4,2)),'] [',tabuleiro_posicao(tab,cria_coordenada(4,3)),'] [',tabuleiro_posicao(tab,cria_coordenada(4,4)),'] ')
        print('Pontuacao:', tabuleiro_pontuacao(tab) )
    else:
        raise ValueError('escreve_tabuleiro: argumentos invalidos')
    
# FUNCOES ADICIONAIS

def pede_jogada():
    """A funcao questiona o utilizador sobre a sua proxima opcao de jogada e devolve-a."""
    jogada = input('Introduza uma jogada (N, S, E, W): ')
    if jogada != 'N' and jogada != 'S' and jogada != 'E' and jogada != 'W':
        print('Jogada invalida.')
        return pede_jogada()
    else:
        return(jogada)
    
def copia_tabuleiro(tab):
    """A funcao devolve um tabuleiro copia do tabuleiro original."""
    tabcopia = [[0,0,0,0],\
                [0,0,0,0],\
                [0,0,0,0],\
                [0,0,0,0],\
                0]
    for l in range(1,5):
        for c in range(1,5):
            tabcopia[l-1][c-1] = tabcopia[l-1][c-1] + tab[l-1][c-1]
    tabcopia[4] = tab[4]
    return tabcopia
    
def preenche_posicao_aleatoria(tab):
    """A funcao devolve o tabuleiro preenchido aleatoriamente com um valor 2 ou 4."""
    opcoes = [2]*4 + [4]
    vazio = tabuleiro_posicoes_vazias(tab)
    coord = vazio[int(random.random()*len(vazio))]
    val = opcoes[int(random.random()*len(opcoes))]
    return tabuleiro_preenche_posicao(tab,coord,val)

# JOGO (PROGRAMA PRINCIPAL)
                
def jogo_2048():
    tab = cria_tabuleiro()
    preenche_posicao_aleatoria(tab)
    preenche_posicao_aleatoria(tab)
    while not tabuleiro_terminado(tab):
        copiatab = copia_tabuleiro(tab)
        escreve_tabuleiro(tab)
        j = pede_jogada()
        tabuleiro_reduz(tab,j)
        while tab == copiatab:
            print('Jogada invalida.')
            j = pede_jogada()
            tabuleiro_reduz(tab,j)
        if tabuleiro_posicoes_vazias(tab) != []:
            preenche_posicao_aleatoria(tab)
    escreve_tabuleiro(tab)
    print('Fim de jogo.')