import random
import interface

NLINHAS  = 4
NCOLUNAS = 4

# TODO: implementar aqui todas as funcoes do enunciado

def desenha_tabuleiro(w, t):
    ''' desenha_tabuleiro : janela x tabuleiro -> {}
        desenha_tabuleiro(t) desenha na janela de jogo o tabuleiro de 2048 t.'''
    
    if not e_tabuleiro(t):
        raise ValueError ('escreve_tabuleiro: argumentos invalidos')
    
    for l in range(1, NLINHAS+1):
        for c in range(1, NCOLUNAS+1):
            w.draw_tile(tabuleiro_posicao(t, cria_coordenada(l, c)), l, c)
        
def joga_2048():
    '''...'''

    w = interface.window_2048()

    # TODO: inicializacao 
    
    quit = False
    
    while not quit:
        desenha_tabuleiro(w, t)
        jogada = w.get_play()
        if jogada == 'Q':
            quit = True

        # TODO: jogo

        w.step()

    print('Jogo terminado.')
    
if __name__ == "__main__":
    joga_2048()
